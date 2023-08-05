from zope.app.component.hooks import getSite
from Products.CMFCore.utils import getToolByName
from pox.banner.content.banner import IBanner
from StringIO import StringIO
import transaction

def setupVarious(context):

    # Ordinarily, GenericSetup handlers check for the existence of XML files.
    # Here, we are not parsing an XML file, but we use this text file as a
    # flag to check that we actually meant for this import step to be run.
    # The file is found in profiles/default.

    if context.readDataFile('pox.banner_various.txt') is None:
        return

    # Add additional setup code here
    out = StringIO()
    portal = getSite()
    acl_users = getToolByName(portal, 'acl_users')
    portal_groups = getToolByName(portal, 'portal_groups')

    if not acl_users.searchGroups(id='Commercials'):
        portal_groups.addGroup('Commercials')
        portal_groups.setRolesForGroup('Commercials', ['Commercial'])
        print >> out, "'Commercials' group created"

    context.getLogger("pox.banner").info(out.getvalue())    
    return out.getvalue()

def reindexBanners(context):
    """ Reindex all Banner objects to store their HTML body as catalog metadata
    """
    
    if context.readDataFile('pox.banner_various.txt') is None:
        return

    # Add additional setup code here
    out = StringIO()
    portal = getSite()
    catalog = getToolByName(portal, 'portal_catalog')
    [banner.getObject().reindexObject() for banner in catalog(object_provides=IBanner.__identifier__)]
    print >> out, "Banners reindexed"
    context.getLogger("pox.banner").info(out.getvalue())    
    return out.getvalue()