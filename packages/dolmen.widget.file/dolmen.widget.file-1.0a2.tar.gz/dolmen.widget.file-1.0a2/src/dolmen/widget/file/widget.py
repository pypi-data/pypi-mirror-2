# -*- coding: utf-8 -*-

import grokcore.view as grok

from dolmen.file import INamedFile, IFileField
from dolmen.widget.file import MF as _
from zeam.form.base import interfaces, NO_VALUE, NO_CHANGE
from zeam.form.base.widgets import DisplayFieldWidget, WidgetExtractor
from zeam.form.ztk.fields import (
    SchemaFieldWidget, SchemaField, registerSchemaField)

from zope.interface import Interface
from zope.location import ILocation
from zope.size.interfaces import ISized
from zope.traversing.browser.absoluteurl import absoluteURL

KEEP = "keep"
DELETE = "delete"
REPLACE = "replace"

grok.templatedir('templates')


class IFileWidget(interfaces.IFieldWidget):
    """A widget that represents a file.
    """


class FileSchemaField(SchemaField):
    """A file field.
    """

registerSchemaField(FileSchemaField, IFileField)


class FileWidget(SchemaFieldWidget):
    grok.implements(IFileWidget)
    grok.adapts(FileSchemaField, interfaces.IFormData, Interface)
    grok.template('input')

    url = None
    filesize = None
    filename = None
    download = None
    allow_action = False

    def prepareContentValue(self, value):
        if value is NO_VALUE or value is None:
            return {self.identifier: False}
        return {self.identifier: True}

    def update(self):
        SchemaFieldWidget.update(self)

        if not self.form.ignoreContent:
            fileobj = self.component._field.get(self.form.context)

            if fileobj:
                self.allow_action = True
                if INamedFile.providedBy(fileobj):
                    self.filename = fileobj.filename
                    self.filesize = ISized(fileobj, None)
                else:
                    self.filename = _(u'download', default=u"Download")

                if ILocation.providedBy(self.form.context):
                    self.url = absoluteURL(self.form.context, self.request)
                    self.download = "%s/++download++%s" % (
                        self.url, self.component.identifier)


class DisplayFileWidget(DisplayFieldWidget):
    grok.implements(IFileWidget)
    grok.adapts(FileSchemaField, interfaces.IFormData, Interface)
    grok.template('display')

    url = None
    filesize = None
    filename = None
    download = None

    def update(self):
        DisplayFieldWidget.update(self)
        fileobj = self.component._field.get(self.form.context)

        if fileobj:
            if INamedFile.providedBy(fileobj):
                self.filename = fileobj.filename
                self.filesize = ISized(fileobj, None)

            self.url = absoluteURL(self.form.context, self.request)
            self.download = "%s/++download++%s" % (
                self.url, self.component.identifier)


class FileWidgetExtractor(WidgetExtractor):
    """A value extractor for a file widget (including image)
    """
    grok.adapts(FileSchemaField, interfaces.IFormData, Interface)

    def extract(self):
        """This method allows us to decide what we do with the different
        options of our field. We handle the 3 options, here :
        keep, replace, delete.
        """
        action = self.request.form.get(self.identifier + '.action', None)
        if action == KEEP:
            # We return a marker that is understood by the form datamanager.
            value = NO_CHANGE
        elif action == DELETE:
            # We explicitly return None instead of  NO_VALUE
            # File storage should take this in consideration
            value = None
        else:
            # Return the value if it exists or a marker uderstood by the
            # form datamanager.
            value = self.request.form.get(self.identifier) or NO_VALUE
        return (value, None)
