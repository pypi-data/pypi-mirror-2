# -*- coding: utf-8 -*-

import grokcore.view as grok
from dolmen.file import IImageField
from dolmen.widget.file import FileWidget, DisplayFileWidget
from dolmen.widget.file import IFileWidget, FileSchemaField
from zeam.form.base.interfaces import IFormData
from zeam.form.ztk.fields import registerSchemaField
from zope.interface import Interface

grok.templatedir('templates')


class IImageWidget(IFileWidget):
    """A widget that represents a file.
    """


class ImageSchemaField(FileSchemaField):
    """An image field.
    """

registerSchemaField(ImageSchemaField, IImageField)


class ImageWidget(FileWidget):
    """A widget for a named file object. It handles specificly an
    image, displaying a thumbnail on both the edit and display form.
    """
    grok.implements(IImageWidget)
    grok.adapts(ImageSchemaField, IFormData, Interface)

    @property
    def preview_url(self):
        if self.form.ignoreContent or not self.url:
            return None
        return '%s/++thumbnail++%s.preview' % (
            self.url, self.component.identifier)


class DisplayImageWidget(DisplayFileWidget):
    """A widget for a named file object. It handles specificly an
    image, displaying a thumbnail on both the edit and display form.
    """
    grok.implements(IImageWidget)
    grok.adapts(ImageSchemaField, IFormData, Interface)

    @property
    def preview_url(self):
        if self.form.ignoreContent or not self.url:
            return None
        return '%s/++thumbnail++%s.preview' % (
            self.url, self.component.identifier)
