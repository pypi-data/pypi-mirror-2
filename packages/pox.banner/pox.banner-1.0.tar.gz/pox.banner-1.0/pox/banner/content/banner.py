'''
Created on 20/09/2009

@author: jpg
'''
from zope import schema

from plone.directives import form

from pox.banner import bannerMessageFactory as _

class IBanner(form.Schema):
    """A Banner
    """
    title = schema.TextLine(title=_(u"Title"),
                            description=_(u"Section title."),
                            required=True)
    body = schema.Text(title=_(u"Banner HTML"),
                       required=True,
                       default=_(u"<h1>Banner code goes here</h1>"))
