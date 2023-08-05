
Let's create a Section object by calling a Factory

    >>> from pox.banner.content.section import *
    >>> first_section = sectionFactory('first_section')
    >>> first_section
    <Section at first_section>
    >>> first_section.id
    'first_section'
    >>> first_section.title = "A sample section"
   
We need to add it to an object manager for acquisition to do its magic.

    >>> self.portal[first_section.id] = first_section
    >>> self.portal.first_section
    <Section at /plone/first_section>

Section can contain sections
   
    >>> first_subsection = sectionFactory('first_subsection')
    >>> first_subsection.title = "A sample subsection"
    >>> self.portal.first_section[first_subsection.id] = first_subsection
    >>> self.portal.first_section.first_subsection
    <Section at /plone/first_section/first_subsection>

Sections have been cataloged.

    >>> from Products.CMFCore.utils import getToolByName
    >>> catalog = getToolByName(self.portal, 'portal_catalog')
    >>> from pox.banner.interfaces import ISection
    >>> [brain.getObject() for brain in catalog(object_provides = ISection.__identifier__)]
    [<Section at /plone/first_section>, <Section at /plone/first_section/first_subsection>]
    
Testing Banner, dexterity content type
We should find the factory first,

    >>> from zope.component import getUtility
    >>> from zope.component.interfaces import IFactory
    >>> bannerFactory = getUtility(IFactory, 'Banner')
    >>> first_banner = bannerFactory('first_banner')
    >>> first_banner.title = 'A banner'
    >>> self.portal.first_section[first_banner.id] = first_banner
    >>> self.portal.first_section.first_banner
    <Item at /plone/first_section/first_banner>

Plone integration...

    >>> self.loginAsPortalOwner()

    >>> self.portal.invokeFactory('Section', 'second_section')
    'second_section'
    >>> self.portal.invokeFactory('Banner', 'second_banner')
    'second_banner'


###########################
## Views memoization
##
###########################

We need a test request...

    >>> from zope.publisher.browser import TestRequest
    >>> request = TestRequest()

And monkey patch the logger to get output in the console...

    >>> import sys
    >>> import logging
    >>> from pox.banner.browser.sectionBanners import logger
    
    >>> logger.setLevel(logging.DEBUG)
    >>> ch = logging.StreamHandler(sys.stdout)
    >>> ch.setLevel(logging.DEBUG)
    >>> formatter = logging.Formatter("%(name)s - %(levelname)s - %(message)s")
    >>> ch.setFormatter(formatter)
    >>> logger.addHandler(ch)
    
    >>> from zope.component import getMultiAdapter
    >>> banners = getMultiAdapter((self.portal.first_section, request), name=u'banners')
    
We call it...

    >>> banners.banners()
    pox.banner - DEBUG - calling banners
    [<Products.ZCatalog.Catalog.mybrains object ...>]
    >>> banners.banners_count()
    pox.banner - DEBUG - calling banners_count
    pox.banner - DEBUG - calling banners
    1
    
And we call it again...

    >>> banners.banners()
    pox.banner - DEBUG - calling banners
    [<Products.ZCatalog.Catalog.mybrains object ...>]
    >>> banners.banners_count()
    pox.banner - DEBUG - calling banners_count
    pox.banner - DEBUG - calling banners
    1
    
Now testing the memoized version...
We need request to be annotatable:

    >>> from zope.interface import directlyProvides
    >>> try:
    ...     from zope.annotation.interfaces import IAttributeAnnotatable
    ... except ImportError:
    ...     from zope.app.annotation.interfaces import IAttributeAnnotatable
    >>> from zope.publisher.interfaces.browser import IDefaultBrowserLayer
    >>> directlyProvides(request, IAttributeAnnotatable, IDefaultBrowserLayer)

    >>> banners = getMultiAdapter((self.portal.first_section, request), name=u'banners_mem')
    
We call it...

    >>> banners.banners()
    pox.banner - DEBUG - calling banners
    [<Products.ZCatalog.Catalog.mybrains object ...>]
    >>> banners.banners_count()
    pox.banner - DEBUG - calling banners_count
    1
    
And we call it again... this time we get the same result
but without calling the method

    >>> banners.banners()
    [<Products.ZCatalog.Catalog.mybrains object ...>]
    >>> banners.banners_count()
    pox.banner - DEBUG - calling banners_count
    1

Creating another banner...

    >>> self.portal.first_section.invokeFactory('Banner', 'another_banner')
    'another_banner'

We still get the memoized value because nothing changes on context and request

    >>> banners.banners()
    [<Products.ZCatalog.Catalog.mybrains object ...>]
    >>> banners.banners_count()
    pox.banner - DEBUG - calling banners_count
    1

    >>> self.portal.first_section.manage_delObjects(['another_banner',])
    
Again with the same request...
    
    >>> banners = getMultiAdapter((self.portal.first_section, request), name=u'banners_mem')
    
Again, we get the correct result without calling the method...

    >>> banners.banners()
    [<Products.ZCatalog.Catalog.mybrains object ...>]
    >>> banners.banners_count()
    pox.banner - DEBUG - calling banners_count
    1
    
And we call it again... this time we get the same result
but without calling the method

    >>> banners.banners()
    [<Products.ZCatalog.Catalog.mybrains object ...>]
    >>> banners.banners_count()
    pox.banner - DEBUG - calling banners_count
    1

Now testing the ram cached version...

    >>> banners = getMultiAdapter((self.portal.first_section, request), name=u'banners_ram')
    
We call it...

    >>> banners.banners()
    pox.banner - DEBUG - calling banners
    [<Products.ZCatalog.Catalog.mybrains object ...>]
    >>> banners.banners_count()
    pox.banner - DEBUG - calling banners_count
    1
    
And we call it again... this time we get the same result
but without calling the method

    >>> banners.banners()
    [<Products.ZCatalog.Catalog.mybrains object ...>]
    >>> banners.banners_count()
    pox.banner - DEBUG - calling banners_count
    1

Again with the same request...
    
    >>> banners = getMultiAdapter((self.portal.first_section, request), name=u'banners_ram')
    
Again, we get the correct result without calling the method...

    >>> banners.banners()
    [<Products.ZCatalog.Catalog.mybrains object ...>]
    >>> banners.banners_count()
    pox.banner - DEBUG - calling banners_count
    1
    
And we call it again... this time we get the same result
but without calling the method

    >>> banners.banners()
    [<Products.ZCatalog.Catalog.mybrains object ...>]
    >>> banners.banners_count()
    pox.banner - DEBUG - calling banners_count
    1

Again with a new request...
    
    >>> request = TestRequest()
    >>> banners = getMultiAdapter((self.portal.first_section, request), name=u'banners_ram')
    
Again, we get the correct result without calling the method...

    >>> banners.banners()
    [<Products.ZCatalog.Catalog.mybrains object ...>]
    >>> banners.banners_count()
    pox.banner - DEBUG - calling banners_count
    1
    
And we call it again... this time we get the same result
but without calling the method

    >>> banners.banners()
    [<Products.ZCatalog.Catalog.mybrains object ...>]
    >>> banners.banners_count()
    pox.banner - DEBUG - calling banners_count
    1

Creating another banner...

    >>> self.portal.first_section.invokeFactory('Banner', 'another_banner')
    'another_banner'

We still get the memoized value because nothing changes on context and request

    >>> banners.banners()
    [<Products.ZCatalog.Catalog.mybrains object ...>]
    >>> banners.banners_count()
    pox.banner - DEBUG - calling banners_count
    1

    >>> import time
    >>> time.sleep(10)
    
    >>> banners.banners()
    pox.banner - DEBUG - calling banners
    [<Products.ZCatalog.Catalog.mybrains object ...>, <Products.ZCatalog.Catalog.mybrains object ...>]
    >>> banners.banners_count()
    pox.banner - DEBUG - calling banners_count
    2

###########################
## Permissions, roles and groups
##
###########################
New permission is available
    >>> len(portal.permission_settings('Manage banners and sections')) > 0
    True

New Commercial role is available

    >>> 'Commercial' in portal.validRoles()
    True
    
And it has just one permission available, the new created one
    >>> [x['name'] for x in portal.permissionsOfRole('Commercial') if x['selected']== 'SELECTED']
    ['Manage banners and sections']
    
Commercials group has Commercial role
	>>> acl_users = getToolByName(portal, 'acl_users')
	>>> len(acl_users.searchGroups(name='Commercials'))
	1
	>>> group = acl_users.getGroupById('Commercials')
	>>> 'Commercial' in group.getRoles()
	True
	
Testing create Sections and Banners

User with Commercial role can add Sections and Banners
    >>> portal.acl_users.userFolderAddUser('commercial', 'secret', ['Commercial'], [])
    >>> self.login('commercial')
    
    >>> portal.invokeFactory('Section', 'commercial_section1')
    'commercial_section1'
    >>> portal.invokeFactory('Banner', 'commercial_banner1')
    'commercial_banner1'
    
User with Contributor role can't add Sections and Banners
    >>> portal.acl_users.userFolderAddUser('contributor', 'secret', ['Contributor'], [])
    >>> self.login('contributor')
    
    >>> portal.invokeFactory('Section', 'commercial_section2')
    Traceback (most recent call last):
    ...
    Unauthorized: Cannot create Section
    
    >>> portal.invokeFactory('Banner', 'commercial_banner2')
    Traceback (most recent call last):
    ...
    Unauthorized: Cannot create Banner

    >>> self.ipython(locals())
