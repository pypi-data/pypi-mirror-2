# -*- coding: iso-8859-15 -*-
"""simple FunkLoad test

$Id: $
"""
import unittest
from collective.funkload import testcase

class Plone(testcase.PloneFLTestCase):
    """XXX

    This test use a configuration file Plone.conf.
    """

    def setUp(self):
        """Setting up test."""
        self.logd("setUp")
        self.server_url = self.conf_get('main', 'url')

    def test_addContent(self):
       
        server_url = self.server_url
        self.plone_login(server_url, 'admin', 'admin', 'Login to portal')
        document_id = self.addContent(
                        server_url, 
                        portal_type='Document', 
                        params=[['id', 'id'],
                                ['title', 'testing title'],
                                ['description', 'testing description'],
                                ['description_text_format', 'text/plain'],
                                ['text_text_format', 'text/html'],
                                ['text_text_format:default', 'text/html'],
                                ['text', 'testing text'],
                                ['text_file', ''],
                                ['language', ''],
                                ['form.submitted', '1'],
                                ['last_referer', ''],
                                ['form_submit', 'Save']], 
                        description='Create document')


        self.get(server_url, description="Visit plone.org")


        # end of test -----------------------------------------------

    def tearDown(self):
        """Setting up test."""
        self.logd("tearDown.\n")

def test_suite():
    return unittest.makeSuite(Plone)


if __name__ in ('main', '__main__'):
    unittest.main()
