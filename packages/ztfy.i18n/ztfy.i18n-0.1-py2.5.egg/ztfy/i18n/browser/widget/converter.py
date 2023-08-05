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

# import Zope3 interfaces
from z3c.form.interfaces import IWidget
from z3c.language.switch.interfaces import II18n

# import local interfaces
from ztfy.file.interfaces import IThumbnailGeometry
from ztfy.i18n.interfaces import II18nField, II18nFileField, II18nCthumbImageField

# import Zope3 packages
from z3c.form.converter import BaseDataConverter, FieldWidgetDataConverter
from zope.app import zapi
from zope.component import adapts

# import local packages


class I18nFieldDataConverter(BaseDataConverter):
    """Base data converter for I18n fields"""

    adapts(II18nField, IWidget)

    def toWidgetValue(self, value):
        return value

    def toFieldValue(self, value):
        result = {}
        langs = self.widget.langs
        for index, lang in enumerate(langs):
            converter = FieldWidgetDataConverter(self.widget.widgets[lang])
            result[lang] = converter.toFieldValue(value[index])
        return result


class I18nFileFieldDataConverter(I18nFieldDataConverter):
    """File data converter for I18n fields"""

    adapts(II18nFileField, IWidget)

    def toFieldValue(self, value):
        result = {}
        langs = self.widget.langs
        for index, lang in enumerate(langs):
            widget = self.widget.widgets[lang]
            if widget.deleted:
                result[lang] = None
            else:
                converter = FieldWidgetDataConverter(widget)
                field_value = converter.toFieldValue(value[index])
                if field_value:
                    result[lang] = field_value
                elif not widget.ignoreContext:
                    result[lang] = II18n(self.widget.context).getAttribute(self.widget.field.getName(), language=lang)
                else:
                    result[lang] = None
        return result


class I18nCthumbImageFieldDataConverter(I18nFileFieldDataConverter):
    """Image data converter for I18n cthumb image fields"""

    adapts(II18nCthumbImageField, IWidget)

    def toFieldValue(self, value):
        result = super(I18nCthumbImageFieldDataConverter, self).toFieldValue(value)
        for lang in result.keys():
            if result[lang] is not None:
                geometry = IThumbnailGeometry(result[lang], None)
                if geometry is not None:
                    position = self.widget.widgets[lang].position
                    if position != geometry.position:
                        geometry.position = position
                    size = self.widget.widgets[lang].size
                    if size != geometry.size:
                        geometry.size = size
        return result
