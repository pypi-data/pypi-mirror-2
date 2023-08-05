# -*- coding: utf-8 -*-

from dolmen.content import schema, name, title, description
from dolmen.content.interfaces import IFactory
from zope.schema.fieldproperty import FieldProperty
from zope.interface import implements, implementedBy


class Factory(object):
    """A content type generic factory.
    """
    implements(IFactory)

    addform = FieldProperty(IFactory['addform'])

    def __init__(self, factory):
        self.factory = factory

    def getInterfaces(self):
        return implementedBy(self.factory)

    def getSchema(self):
        return schema.bind().get(self.factory)

    @property
    def name(self):
        """This, by default, returns the `name\ directive value,
        that is used as __content_type__.
        """
        return name.bind().get(self.factory)

    @property
    def title(self):
        return title.bind().get(self.factory)

    @property
    def description(self):
        return description.bind().get(self.factory)

    def __call__(self, *args, **kw):
        return self.factory(*args, **kw)
