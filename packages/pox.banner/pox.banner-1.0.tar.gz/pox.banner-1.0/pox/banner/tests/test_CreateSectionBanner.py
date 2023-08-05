# -*- coding: iso-8859-15 -*-
"""create_folders FunkLoad test

$Id: $
"""
import unittest
try:
    from funkload.Lipsum import Lipsum, V_ASCII, CHARS, SEP
    from collective.funkload import testcase
    
    class CreateSectionBanner(testcase.FLTestCase):
        """XXX
    
        This test use a configuration file CreateSectionBanner.conf.
        """
    
        def setUp(self):
            """Setting up test."""
            self.logd("setUp")
            self.server_url = self.conf_get('main', 'url')
            self.lipsum = Lipsum(vocab=V_ASCII, chars=CHARS, sep=SEP)
            
            self.post(self.server_url + "/pox.banner.tests/login_form", 
                      params=[['form.submitted', '1'],
                              ['js_enabled', '0'],
                              ['cookies_enabled', '0'],
                              ['login_name', ''],
                              ['pwd_empty', '0'],
                              ['came_from', 'login_success'],
                              ['__ac_name', 'admin'],
                              ['__ac_password', 'admin']],
                      description="Login as manager")
    
        def test_create_section_banner(self):
            # The description should be set in the configuration file
            server_url = self.server_url
            # begin of test ---------------------------------------------
    
            self.get(self.server_url + "/pox.banner.tests/+/addSection",
                     description="Get Section add form")
            
            section = self.post(self.server_url + "/pox.banner.tests/+/addSection", 
                                params=[['form.title', 'Section1'],
                                        ['form.actions.save', 'Save']],
                                description="Saving Section add form")
            section_url = server_url + section.url.rsplit('/', 1)[0]
            
            self.get(section_url + "/++add++Banner",
                     description="Get Banner add form")
            
            banner = self.post(section_url + "/++add++Banner", 
                               params=[['form.widgets.title', 'Banner1'],
                                       ['form.widgets.body', 
                                        "<p>%s</p>" % self.lipsum.getMessage(length=20)],
                                       ['form.buttons.save', 'Save']],
                               description="Saving Banner add form")
             # end of test -----------------------------------------------
    
        def create_atfolder(self):
            sb_url = self.server_url + '/pox.banner.tests/sb'
            if not self.exists(sb_url):
                createObject = self._browse(self.server_url + 
                                            "/pox.banner.tests/createObject?type_name=Folder",
                                            method='get', 
                                            follow_redirect=False,
                                            description="Get /pox.banner.tests/createObject")
        
                sb = self.post(createObject.headers.get('Location'), params=[
                    ['id', createObject.headers.get('Location').split('/')[-2]],
                    ['title', 'sb'],
                    ['description', ''],
                    ['description_text_format', 'text/plain'],
                    ['subject_keywords:lines', ''],
                    ['subject_existing_keywords:default:list', ''],
                    ['location', ''],
                    ['language', ''],
                    ['effectiveDate', ''],
                    ['effectiveDate_year', '0000'],
                    ['effectiveDate_month', '00'],
                    ['effectiveDate_day', '00'],
                    ['effectiveDate_hour', '12'],
                    ['effectiveDate_minute', '00'],
                    ['effectiveDate_ampm', 'AM'],
                    ['expirationDate', ''],
                    ['expirationDate_year', '0000'],
                    ['expirationDate_month', '00'],
                    ['expirationDate_day', '00'],
                    ['expirationDate_hour', '12'],
                    ['expirationDate_minute', '00'],
                    ['expirationDate_ampm', 'AM'],
                    ['creators:lines', 'admin'],
                    ['contributors:lines', ''],
                    ['rights', ''],
                    ['rights_text_format', 'text/html'],
                    ['allowDiscussion:boolean:default', ''],
                    ['excludeFromNav:boolean:default', ''],
                    ['nextPreviousEnabled:boolean:default', ''],
                    ['fieldsets:list', 'default'],
                    ['fieldsets:list', 'categorization'],
                    ['fieldsets:list', 'dates'],
                    ['fieldsets:list', 'ownership'],
                    ['fieldsets:list', 'settings'],
                    ['form.submitted', '1'],
                    ['add_reference.field:record', ''],
                    ['add_reference.type:record', ''],
                    ['add_reference.destination:record', ''],
                    ['last_referer', 'http://localhost:8080/pox.banner.tests'],
                    ['form.button.save', 'Save']],
                    description="Post /pox.banner.tests/port...144378603/atct_edit")
                
        def tearDown(self):
            """Setting up test."""
            self.logd("tearDown.\n")
except:
    CreateSectionBanner = unittest.TestCase
    
def test_suite():
    suite = unittest.makeSuite(CreateSectionBanner)
    suite.level = 5
    return suite

if __name__ in ('main', '__main__'):
    unittest.main()
