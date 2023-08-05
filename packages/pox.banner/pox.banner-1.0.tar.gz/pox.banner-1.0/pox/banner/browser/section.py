import zope.formlib
from five import grok
from zope.component import createObject
from Acquisition import aq_base

from Products.Five.formlib import formbase as fiveformbase
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from plone.app.form import base as formbase
from plone.directives import form

from pox.banner import interfaces

class Add(formbase.AddForm):
    form_fields = zope.formlib.form.FormFields(interfaces.ISection)

    def create(self, data):
        content = createObject(self.__name__)
        zope.formlib.form.applyChanges(content, self.form_fields, data)
        return aq_base(content)

class Edit(formbase.EditForm):
    form_fields = zope.formlib.form.FormFields(interfaces.ISection)

class View(fiveformbase.DisplayForm):
    form_fields = zope.formlib.form.FormFields(interfaces.ISection)

class z3cEdit(form.SchemaEditForm):
    grok.context(interfaces.ISection)

class z3cDisplay(form.DisplayForm):
    grok.context(interfaces.ISection)
    template = ViewPageTemplateFile('section.pt')
