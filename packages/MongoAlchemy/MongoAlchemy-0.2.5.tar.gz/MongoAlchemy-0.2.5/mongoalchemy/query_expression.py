# The MIT License
# 
# Copyright (c) 2010 Jeffrey Jenkins
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

from mongoalchemy.fields import BadValueException

class BadQueryException(Exception):
    ''' Raised when a method would result in a query which is not well-formed.
    '''
    pass

class QueryFieldSet(object):
    ''' Intermediate class used to allow access to create QueryField objects 
        from a subclass of Document.  Should generally be indirectly accessed 
        via ``Document.f``.
    '''
    def __init__(self, type, fields, parent=None):
        self.type = type
        self.fields = fields
        self.parent = parent
    
    def __getattr__(self, name):
        if name not in self.fields:
            raise BadQueryException('%s is not a field in %s' % (name, self.type.class_name()))
        return QueryField(name, self.fields[name], parent=self.parent)

class QueryField(object):
    def __init__(self, name, type, parent=None):
        self.__name = name
        self.__type = type
        self.__parent = parent
    
    def _get_parent(self):
        return self.__parent
    
    def get_name(self):
        ''' Gets the MongoDB field name for the :class:`mongoalchemy.fields.Field`
            this QueryField is wrapping'''
        return self.__type.db_field
    
    def get_type(self):
        ''' Returns the underlying :class:`mongoalchemy.fields.Field` '''
        return self.__type
    
    def __getattr__(self, name):
        fields = self.__type.type.get_fields()
        if name not in fields:
            raise BadQueryException('%s is not a field in %s' % (name, str(self)))
        return QueryField(name, fields[name], parent=self)
    
    @property
    def f(self):
        ''' ``f`` provides acces to the sub-fields of this field.  They can 
            also be accessed directly if they do not interfere with an 
            attribute of :class:`QueryField`.
            
            **Example**: ``SomeDoc.f.outer_field.f.inner_field`` is the same as ``SomeDoc.f.outer_field.inner_field``
        '''
        fields = self.__type.type.get_fields()
        return QueryFieldSet(self.__type, fields, parent=self)
    
    def __absolute_name(self):
        res = []
        current = self
        while current:
            res.append(current.get_name())
            current = current._get_parent()
        return '.'.join(reversed(res))
    
    def in_(self, *values):
        ''' A query to check if this query field is one of the values 
            in ``values``.  Produces a MongoDB ``$in`` expression.
        '''
        return QueryExpression({
            str(self) : { '$in' : values }
        })
    
    def __str__(self):
        return self.__absolute_name()
    
    def __eq__(self, value):
        return self.eq_(value)
    def eq_(self, value):
        ''' Creates a query expression where ``this field == value`` 
        
            .. note:: The prefered usage is via an operator: ``User.f.name == value``
        '''
        if not self.__type.is_valid_wrap(value):
            raise BadQueryException('Invalid "value" for comparison against %s: %s' % (str(self), value))
        return QueryExpression({ self.__absolute_name() : value })
    
    def __lt__(self, value):
        return self.lt_(value)
    def lt_(self, value):
        ''' Creates a query expression where ``this field < value`` 
        
            .. note:: The prefered usage is via an operator: ``User.f.name < value``
        '''
        return self.__comparator('$lt', value)
    
    def __le__(self, value):
        return self.le_(value)
    def le_(self, value):
        ''' Creates a query expression where ``this field <= value`` 
        
            .. note:: The prefered usage is via an operator: ``User.f.name <= value``
        '''
        return self.__comparator('$lte', value)
    
    def __ne__(self, value):
        return self.ne_(value)
    def ne_(self, value):
        ''' Creates a query expression where ``this field != value`` 
        
            .. note:: The prefered usage is via an operator: ``User.f.name != value``
        '''
        return self.__comparator('$ne', value)
    
    def __gt__(self, value):
        return self.gt_(value)
    def gt_(self, value):
        ''' Creates a query expression where ``this field > value`` 
        
            .. note:: The prefered usage is via an operator: ``User.f.name > value``
        '''
        return self.__comparator('$gt', value)
    
    def __ge__(self, value):
        return self.ge_(value)
    def ge_(self, value):
        ''' Creates a query expression where ``this field >= value`` 
        
            .. note:: The prefered usage is via an operator: ``User.f.name >= value``
        '''
        return self.__comparator('$gte', value)
    
    def __comparator(self, op, value):
        try:
            return QueryExpression({
                self.__absolute_name() : {
                    op : self.__type.wrap(value)
                }
            })
        except BadValueException:
            raise BadQueryException('Invalid "value" for %s comparison against %s: %s' % (self, op, value))

class QueryExpression(object):
    ''' A QueryExpression wraps a dictionary representing a query to perform 
        on a mongo collection.  The 
    
        .. note:: There is no ``and_`` expression because multiple expressions
            can be specified to a single call of :func:`Query.filter`
    '''
    def __init__(self, obj):
        self.obj = obj
    def not_(self):
        '''Negates this instance's query expression using MongoDB's ``$not`` 
            operator
            
            **Example**: ``(User.f.name == 'Jeff').not_()``
            
            .. note:: Another usage is via an operator, but parens are needed 
                to get past precedence issues: ``~ (User.f.name == 'Jeff')``
            '''

        return QueryExpression({
                '$not' : self.obj
            })
    
    def __invert__(self):
        return self.not_()
    
    def __or__(self, expression):
        return self.or_(expression)
    
    def or_(self, expression):
        ''' Adds the given expression to this instance's MongoDB ``$or`` 
            expression, starting a new one if one does not exst
            
            **Example**: ``(User.f.name == 'Jeff').or_(User.f.name == 'Jack')``
            
            .. note:: The prefered usageis via an operator: ``User.f.name == 'Jeff' | User.f.name == 'Jack'``
            
            '''
        
        if '$or' in self.obj:
            self.obj['$or'].append(expression.obj)
            return self
        self.obj = {
            '$or' : [self.obj, expression.obj]
        }
        return self
