from zope.schema import List
##############################################################################
#
# Copyright (c) 2001, 2002 Zope Foundation and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
"""This set of tests exercises Object fields.

$Id: test_objectfield.py 111614 2010-04-30 13:36:09Z gotcha $
"""
from unittest import TestSuite, main, makeSuite

import zope.event
from zope.interface import Attribute, Interface, implements
from zope.schema import Object, TextLine
from zope.schema.fieldproperty import FieldProperty
from zope.schema.interfaces import ValidationError
from zope.schema.interfaces import RequiredMissing, WrongContainedType
from zope.schema.interfaces import WrongType, SchemaNotFullyImplemented
from zope.schema.tests.test_field import FieldTestBase
from zope.schema.interfaces import IBeforeObjectAssignedEvent
from zope.testing.cleanup import CleanUp

from zope.schema._messageid import _


class ITestSchema(Interface):
    """A test schema"""

    foo = TextLine(
        title=_(u"Foo"),
        description=_(u"Foo description"),
        default=u"",
        required=True)

    bar = TextLine(
        title=_(u"Bar"),
        description=_(u"Bar description"),
        default=u"",
        required=False)

    attribute = Attribute("Test attribute, an attribute can't be validated.")


class ICyclic(Interface):
    """A test schema"""

    baz = Object(
        schema=Interface,
        title=_(u"Baz"),
        description=_(u"Baz description"),
        required=False,
        )

    baz_list = List(
        value_type=Object(schema=Interface),
        title=_(u"Baz List"),
        description=_(u"Baz description"),
        required=False,
        )


class IBaz(Interface):
    """A test schema"""

    cyclic = Object(
        schema=ICyclic,
        title=_(u"Cyclic"),
        description=_(u"Cyclic description"),
        required=False,
        )

ICyclic['baz'].schema = IBaz
ICyclic['baz_list'].value_type.schema = IBaz


class Cyclic(object):

    implements(ICyclic)

    def __init__(self, baz, baz_list):
        self.baz = baz
        self.baz_list = baz_list


class Baz(object):

    implements(IBaz)

    def __init__(self, cyclic):
        self.cyclic = cyclic


class TestClass(object):

    implements(ITestSchema)

    _foo = u''
    _bar = u''
    _attribute = u''

    def getfoo(self):
        return self._foo

    def setfoo(self, value):
        self._foo = value

    foo = property(getfoo, setfoo, None, u'foo')

    def getbar(self):
        return self._bar

    def setbar(self, value):
        self._bar = value

    bar = property(getbar, setbar, None, u'foo')

    def getattribute(self):
        return self._attribute

    def setattribute(self, value):
        self._attribute = value

    attribute = property(getattribute, setattribute, None, u'attribute')


class FieldPropertyTestClass(object):

    implements(ITestSchema)


    foo = FieldProperty(ITestSchema['foo'])
    bar = FieldProperty(ITestSchema['bar'])
    attribute = FieldProperty(ITestSchema['attribute'])


class NotFullyImplementedTestClass(object):

    implements(ITestSchema)

    foo = FieldProperty(ITestSchema['foo'])
    # bar = FieldProperty(ITestSchema['bar']): bar is not implemented
    # attribute


class ObjectTest(CleanUp, FieldTestBase):
    """Test the Object Field."""

    def getErrors(self, f, *args, **kw):
        try:
            f(*args, **kw)
        except WrongContainedType, e:
            try:
                return e[0]
            except:
                return []
        self.fail('Expected WrongContainedType Error')

    def makeTestObject(self, **kw):
        kw['schema'] = kw.get('schema', Interface)
        return Object(**kw)

    _Field_Factory = makeTestObject

    def makeTestData(self):
        return TestClass()

    def makeFieldPropertyTestClass(self):
        return FieldPropertyTestClass()

    def makeNotFullyImplementedTestData(self):
        return NotFullyImplementedTestClass()

    def invalidSchemas(self):
        return ['foo', 1, 0, {}, [], None]

    def validSchemas(self):
        return [Interface, ITestSchema]

    def test_init(self):
        for schema in self.validSchemas():
            Object(schema=schema)
        for schema in self.invalidSchemas():
            self.assertRaises(ValidationError, Object, schema=schema)
            self.assertRaises(WrongType, Object, schema=schema)

    def testValidate(self):
        # this test of the base class is not applicable
        pass

    def testValidateRequired(self):
        # this test of the base class is not applicable
        pass

    def test_validate_required(self):
        field = self._Field_Factory(
            title=u'Required field', description=u'',
            readonly=False, required=True)
        self.assertRaises(RequiredMissing, field.validate, None)

    def test_validate_TestData(self):
        field = self.makeTestObject(schema=ITestSchema, required=False)
        data = self.makeTestData()
        field.validate(data)
        field = self.makeTestObject(schema=ITestSchema)
        field.validate(data)
        data.foo = None
        self.assertRaises(ValidationError, field.validate, data)
        self.assertRaises(WrongContainedType, field.validate, data)
        errors = self.getErrors(field.validate, data)
        self.assertEquals(errors[0], RequiredMissing('foo'))

    def test_validate_FieldPropertyTestData(self):
        field = self.makeTestObject(schema=ITestSchema, required=False)
        data = self.makeFieldPropertyTestClass()
        field.validate(data)
        field = self.makeTestObject(schema=ITestSchema)
        field.validate(data)
        self.assertRaises(ValidationError, setattr, data, 'foo', None)
        self.assertRaises(RequiredMissing, setattr, data, 'foo', None)

    def test_validate_NotFullyImplementedTestData(self):
        field = self.makeTestObject(schema=ITestSchema, required=False)
        data = self.makeNotFullyImplementedTestData()
        self.assertRaises(ValidationError, field.validate, data)
        self.assertRaises(WrongContainedType, field.validate, data)
        errors = self.getErrors(field.validate, data)
        self.assert_(isinstance(errors[0], SchemaNotFullyImplemented))

    def test_beforeAssignEvent(self):
        field = self.makeTestObject(schema=ITestSchema, required=False,
                                    __name__='object_field')
        data = self.makeTestData()
        events = []

        def register_event(event):
            events.append(event)
        zope.event.subscribers.append(register_event)

        class Dummy(object):
            pass
        context = Dummy()
        field.set(context, data)
        self.assertEquals(1, len(events))
        event = events[0]
        self.failUnless(IBeforeObjectAssignedEvent.providedBy(event))
        self.assertEquals(data, event.object)
        self.assertEquals('object_field', event.name)
        self.assertEquals(context, event.context)

    # cycles

    def test_with_cycles_validate(self):
        field = self.makeTestObject(schema=ICyclic)
        baz1 = Baz(None)
        baz2 = Baz(None)
        cyclic = Cyclic(baz1, [baz1, baz2])
        baz1.cyclic = cyclic
        baz2.cyclic = cyclic
        field.validate(cyclic)

    def test_with_cycles_object_not_valid(self):
        field = self.makeTestObject(schema=ICyclic)
        data = self.makeTestData()
        baz1 = Baz(None)
        baz2 = Baz(None)
        baz3 = Baz(data)
        cyclic = Cyclic(baz3, [baz1, baz2])
        baz1.cyclic = cyclic
        baz2.cyclic = cyclic
        self.assertRaises(WrongContainedType, field.validate, cyclic)

    def test_with_cycles_collection_not_valid(self):
        field = self.makeTestObject(schema=ICyclic)
        data = self.makeTestData()
        baz1 = Baz(None)
        baz2 = Baz(None)
        baz3 = Baz(data)
        cyclic = Cyclic(baz1, [baz2, baz3])
        baz1.cyclic = cyclic
        baz2.cyclic = cyclic
        self.assertRaises(WrongContainedType, field.validate, cyclic)


def test_suite():
    suite = TestSuite()
    suite.addTest(makeSuite(ObjectTest))
    return suite

if __name__ == '__main__':
    main(defaultTest='test_suite')
