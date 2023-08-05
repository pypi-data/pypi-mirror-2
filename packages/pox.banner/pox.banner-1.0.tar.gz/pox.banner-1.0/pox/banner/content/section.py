'''
Created on 19/09/2009

@author: jpg
'''
from zope.interface import implements
from zope.component.factory import Factory
from plone.app.content.container import Container
from plone.app.content.interfaces import INameFromTitle
from Products.Archetypes.Referenceable import Referenceable
from pox.banner import interfaces

from OFS.interfaces import IOrderedContainer
from OFS.OrderSupport import OrderSupport

class Section(Container, Referenceable, OrderSupport):
    """
    A section to contain other sections or banners
    """
    implements(interfaces.ISection, INameFromTitle)
    portal_type = "Section"
    title = u""

sectionFactory = Factory(Section, 'Section',
                         ' A section to contain other sections or banners')
