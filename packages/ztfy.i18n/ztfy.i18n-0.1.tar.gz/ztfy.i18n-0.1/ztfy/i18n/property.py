### -*- coding: utf-8 -*- ####################################################
##############################################################################
#
# Copyright (c) 2008 Thierry Florac <tflorac AT ulthar.net>
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


# import standard packages
import transaction
try:
    import magic
except:
    magic = None

# import Zope3 interfaces
from zope.app.file.interfaces import IFile
from zope.location.interfaces import ILocation

# import local interfaces
from interfaces import II18nFilePropertiesContainer, II18nFilePropertiesContainerAttributes, II18nField

# import Zope3 packages
from zope.app.container.contained import ObjectAddedEvent, ObjectRemovedEvent
from zope.app.file import File, Image
from zope.interface import alsoProvides
from zope.event import notify
from zope.lifecycleevent import ObjectCreatedEvent
from zope.location import locate
from zope.security.proxy import removeSecurityProxy

# import local packages
from ztfy.utils.traversing import getParent
from ztfy.utils.unicode import uninvl, unidict

from ztfy.i18n import _


_marker = dict()

if magic is not None:
    _magic = magic.open(magic.MAGIC_MIME)
    _magic.load()


class I18nProperty(object):
    """Base class for I18n properties"""

    def __init__(self, field, name=None, converters=(), value_converters=()):
        if not II18nField.providedBy(field):
            raise ValueError, _("Provided field must implement II18nField interface...")
        if name is None:
            name = field.__name__
        self.__field = field
        self.__name = name
        self.__converters = converters
        self.__value_converters = value_converters

    def __get__(self, instance, klass):
        if instance is None:
            return self
        value = instance.__dict__.get(self.__name, _marker)
        if value is _marker:
            field = self.__field.bind(instance)
            value = getattr(field, 'default', _marker)
            if value is _marker:
                raise AttributeError(self.__name)
        return value

    def __set__(self, instance, value):
        for converter in self.__converters:
            value = converter(value)
        for converter in self.__value_converters:
            for lang in value:
                value[lang] = converter(value[lang])
        field = self.__field.bind(instance)
        field.validate(value)
        if field.readonly and instance.__dict__.has_key(self.__name):
            raise ValueError(self.__name, _("Field is readonly"))
        old_value = instance.__dict__.get(self.__name, _marker)
        if old_value is _marker:
            old_value = self.__field.default.copy()
        for k in value:
            old_value[k] = value[k]
        instance.__dict__[self.__name] = old_value

    def __getattr__(self, name):
        return getattr(self.__field, name)


class I18nTextProperty(I18nProperty):
    """I18n property to handle Text and TextLine values"""

    def __init__(self, field, name=None, converters=(), value_converters=()):
        super(I18nTextProperty, self).__init__(field, name, converters=converters,
                                              value_converters=(uninvl,) + value_converters)


class I18nFileProperty(I18nProperty):
    """I18n property to handle files"""

    def __init__(self, field, name=None, converters=(), value_converters=(), klass=File, img_klass=None, **args):
        super(I18nFileProperty, self).__init__(field, name, converters, value_converters)
        self.__klass = klass
        self.__img_klass = img_klass
        self.__args = args

    def __set__(self, instance, value):
        for converter in self._I18nProperty__converters:
            value = converter(value)
        for converter in self._I18nProperty__value_converters:
            for lang in value:
                value[lang] = converter(value[lang])
        for lang in value:
            if value[lang] is not None:
                if not IFile.providedBy(value[lang]):
                    content_type = 'text/plain'
                    if magic is not None:
                        content_type = _magic.buffer(value[lang][:4096])
                    if (self.__img_klass is not None) and content_type.startswith('image/'):
                        f = self.__img_klass(**self.__args)
                    else:
                        f = self.__klass(**self.__args)
                    notify(ObjectCreatedEvent(f))
                    f.data = value[lang]
                    if magic is not None:
                        f.contentType = content_type
                    value[lang] = f
        field = self._I18nProperty__field.bind(instance)
        field.validate(value)
        if field.readonly and instance.__dict__.has_key(self.__name):
            raise ValueError(self._I18nProperty__name, _("Field is readonly"))
        old_value = instance.__dict__.get(self._I18nProperty__name, _marker)
        if old_value is _marker:
            old_value = self._I18nProperty__field.default.copy()
        for k in value:
            old_file = old_value.get(k, _marker)
            new_file = value[k]
            if old_file != new_file:
                if (old_file is not _marker) and (old_file is not None):
                    notify(ObjectRemovedEvent(old_file))
                if new_file is not None:
                    filename = '++i18n++%s:%s' % (self._I18nProperty__name, k)
                    locate(new_file, removeSecurityProxy(instance), filename)
                    alsoProvides(new_file, ILocation)
                    alsoProvides(instance, II18nFilePropertiesContainer)
                    II18nFilePropertiesContainerAttributes(instance).attributes.add(self._I18nProperty__name)
                    notify(ObjectAddedEvent(new_file, instance, filename))
                old_value[k] = new_file
        instance.__dict__[self._I18nProperty__name] = old_value


class I18nImageProperty(I18nFileProperty):
    """I18n property to handle images"""

    def __init__(self, field, name=None, converters=(), value_converters=(), klass=Image, img_klass=None, **args):
        super(I18nImageProperty, self).__init__(field, name, converters, value_converters, klass, img_klass, **args)
