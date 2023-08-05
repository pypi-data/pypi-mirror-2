'''
Created on 19/09/2009

@author: jpg
'''
from zope import schema
from zope.interface import Interface

from pox.banner import bannerMessageFactory as _

class ISection(Interface):
    """A Section
    """
    title = schema.TextLine(title=_(u"Title"),
                            description=_(u"Section title."),
                            required=True)
