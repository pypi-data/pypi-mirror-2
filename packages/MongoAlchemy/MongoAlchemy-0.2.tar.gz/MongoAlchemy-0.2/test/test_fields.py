from nose.tools import *
from pprint import pprint
from mongoalchemy.fields import *
from test.util import known_failure
from datetime import datetime

# Field Tests

@raises(NotImplementedError)
def test_unimplemented_wrap():
    Field().wrap({})

@raises(NotImplementedError)
def test_unimplemented_unwrap():
    Field().unwrap({})

@raises(NotImplementedError)
def test_unimplemented_is_valid_wrap():
    Field().is_valid_wrap({})

@raises(NotImplementedError)
def test_unimplemented_is_valid_wrap():
    Field().is_valid_wrap({})

@raises(BadValueException)
def test_validate_unwrap_fail():
    StringField().unwrap(4)

# String Tests
@raises(BadValueException)
def string_wrong_type_test():
    StringField().wrap(4)

@raises(BadValueException)
def string_too_long_test():
    StringField(max_length=4).wrap('12345')

@raises(BadValueException)
def string_too_short_test():
    StringField(min_length=4).wrap('123')

def string_value_test():
    s = StringField()
    assert s.wrap('foo') == 'foo'
    assert s.unwrap('bar') == 'bar'

# Bool Field
@raises(BadValueException)
def bool_wrong_type_test():
    BoolField().wrap(4)

def bool_value_test():
    b = BoolField()
    assert b.wrap(True) == True
    assert b.unwrap(False) == False

# Number Fields
@raises(BadValueException)
def int_wrong_type_test():
    IntField().wrap('4')

@raises(BadValueException)
def int_too_high_test():
    IntField(max_value=4).wrap(5)

@raises(BadValueException)
def int_too_low_test():
    IntField(min_value=4).wrap(3)

def int_value_test():
    s = IntField()
    assert s.wrap(1) == 1
    assert s.unwrap(1564684654) == 1564684654

@raises(BadValueException)
def float_wrong_type_test():
    FloatField().wrap(1)

# Date/time field
@raises(BadValueException)
def datetime_wrong_type_test():
    DateTimeField().wrap(4)

@raises(BadValueException)
def datetime_too_new_test():
    DateTimeField(max_value=datetime(2009, 7, 9)).wrap(datetime(2009, 7, 10))

@raises(BadValueException)
def datetime_too_old_test():
    DateTimeField(min_value=datetime(2009, 7, 9)).wrap(datetime(2009, 7, 8))

def datetime_value_test():
    s = DateTimeField()
    assert s.wrap(datetime(2009, 7, 9)) == datetime(2009, 7, 9)
    assert s.unwrap(datetime(2009, 7, 9)) == datetime(2009, 7, 9)

# Anything Field
def test_anything():
    a = AnythingField()
    foo = {'23423423' : [23423432], 'fvfvf' : { 'a' : [] }}
    assert a.is_valid_wrap(foo)
    assert a.unwrap(a.wrap(foo)) == foo

#ObjectID Field
@raises(BadValueException)
def objectid_wrong_type_test():
    from pymongo.objectid import ObjectId
    ObjectIdField().wrap(1)

@raises(BadValueException)
def objectid_wrong_type_unwrap_test():
    from pymongo.objectid import ObjectId
    ObjectIdField().unwrap(1)

def objectid_value_test():
    from pymongo.objectid import ObjectId
    o = ObjectIdField()
    oid = ObjectId('4c9e2587eae7dd6064000000')
    assert o.unwrap(o.wrap(oid)) == oid

