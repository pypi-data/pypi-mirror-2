from zope.interface import Interface, implements

from Products.Five.browser import BrowserView
from Products.CMFCore.utils import getToolByName
from pox.banner.content.banner import IBanner
from Acquisition import aq_inner
import logging
from plone.memoize import ram, view
from time import time

RAM_CACHE_SECONDS = 10
logger = logging.getLogger('pox.banner')

class ISectionBanners(Interface):
    """
    Retrieve section's contained banners
    """
    
    def banners():
        """
        Get contained banners
        """

    def banners_count():
        """
        Get banners count
        """


class SectionBanners( BrowserView ):
    """
    Helper view to test code caching techniques
    """
    implements(ISectionBanners)
    def __init__(self, context, request):
        self.context = context
        self.request = request

    def banners(self):
        """
        The actual search
        """
        logger.log(logging.DEBUG, 'calling banners')
        context = aq_inner(self.context)
        catalog = getToolByName(context, 'portal_catalog')
        query = dict(object_provides = IBanner.__identifier__)
        query['path'] = { 'query': '/'.join(context.getPhysicalPath()),
                          'depth': 1 }
        brains = catalog(query)

        return brains

    def banners_count(self):
        """
        Tells how many banners we found
        """
        logger.log(logging.DEBUG, 'calling banners_count')
        return len(self.banners())

class SectionBannersMem( SectionBanners ):
    """
    Alternative implementation of the SectionBanners class
    """

    @view.memoize
    def banners(self):
        """
        Decorated. It just calls SectionBanners' banners().
        """
        return super(SectionBannersMem, self).banners()

class SectionBannersRam( SectionBanners ):
    """
    Alternative implementation of the SectionBanners class
    """

    def _banners_cachekey(method, self, **args):
        """
        Returns key used by @ram.cache.
        """
        the_key = list(self.context.getPhysicalPath())
        the_key.append(time() // RAM_CACHE_SECONDS)
        return the_key

    @ram.cache(_banners_cachekey)
    def banners(self):
        """
        Decorated. It just calls SectionBanners' banners().
        """
        return super(SectionBannersRam, self).banners()

class SectionBannersVol( SectionBanners ):
    """
    Alternative implementation of the SectionBanners class
    """

    def banners(self):
        """
        It just calls SectionBanners' banners() when needed.
        """
        the_banners = getattr(self, '_v_banners', None)
        if the_banners is None:
            the_banners = super(SectionBannersVol, self).banners()
            self._v_banners = the_banners
        return the_banners
