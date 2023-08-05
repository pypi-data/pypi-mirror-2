################################################################################
#
# Copyright (c) 2002-2005, Benjamin Saller <bcsaller@ideasuite.com>, and
#                              the respective authors. All rights reserved.
# For a list of Archetypes contributors see docs/CREDITS.txt.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# * Redistributions of source code must retain the above copyright notice, this
#   list of conditions and the following disclaimer.
# * Redistributions in binary form must reproduce the above copyright notice,
#   this list of conditions and the following disclaimer in the documentation
#   and/or other materials provided with the distribution.
# * Neither the name of the author nor the names of its contributors may be used
#   to endorse or promote products derived from this software without specific
#   prior written permission.
#
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
################################################################################
"""
"""

import time

from Products.Archetypes.tests.atsitetestcase import ATFunctionalSiteTestCase
from Products.Archetypes.atapi import *
from Products.Archetypes.tests.attestcase import default_user
from Products.Archetypes.tests.atsitetestcase import portal_owner

from StringIO import StringIO

html = """\
<html>
<head><title>Foo</title></head>
<body>Bar</body>
</html>
"""

class TestFunctionalObjectCreation(ATFunctionalSiteTestCase):
    """Tests object renaming and creation"""

    def afterSetUp(self):
        # basic data
        self.folder_url = self.folder.absolute_url()
        self.folder_path = '/%s' % self.folder.absolute_url(1)
        self.basic_auth = '%s:secret' % default_user
        self.owner_auth = '%s:secret' % portal_owner
        # We want 401 responses, not redirects to a login page
        if hasattr(self.portal.aq_base, 'cookie_authentication'):
            self.portal._delObject('cookie_authentication')

        # disable portal_factory as it's a nuisance here
        if hasattr(self.portal.aq_base, 'portal_factory'):
            self.portal.portal_factory.manage_setPortalFactoryTypes(listOfTypeIds=[])

        # error log
        from Products.SiteErrorLog.SiteErrorLog import temp_logs
        temp_logs.clear() # clean up log
        self.error_log = self.portal.error_log
        self.error_log._ignored_exceptions = ()

        self.setupCTR()

    def setupCTR(self):
        #Modify the CTR to point to SimpleType
        ctr = self.portal.content_type_registry
        if ctr.getPredicate('text'):
            # ATCT has a predict
            ctr.removePredicate('text')
        ctr.addPredicate('text', 'major_minor' )
        ctr.getPredicate('text' ).edit('text', '' )
        ctr.assignTypeName('text', 'DDocument')
        ctr.reorderPredicate('text', 0)

        return ctr

    def assertStatusEqual(self, a, b, msg=''):
        """Helper method that uses the error log to output useful debug infos
        """
        now = time.time()
        if a != b:
            entries = self.error_log.getLogEntries()
            if entries:
                msg = entries[0]['tb_text']
            else:
                if not msg:
                    msg = 'no error log msg available'
                    self.failUnlessEqual(a, b)
        self.failUnlessEqual(a, b, msg)

    def test_id_change_with_non_auto_id(self):
        """Make sure Id is only set when original id is autogenerated"""
        # Make our content type use auto generated ids
        from Products.Archetypes.examples.DDocument import DDocument
        DDocument._at_rename_after_creation = True
    
        auto_id='orig_id'
    
        # create an object with an autogenerated id
        response = self.publish(self.folder_path +
                                '/invokeFactory?type_name=DDocument&id=%s'%auto_id,
                                self.basic_auth)
    
        # XXX now lets test if http://plone.org/collector/4487 is present
        if  "base_edit.cpt" in self.portal.portal_skins.archetypes.objectIds():
            raise AttributeError, ("test_id_change_with_non_auto_id "
                  "is expected to fail unless  http://plone.org/collector/4487 is fixed")
    
        self.failUnless(auto_id in self.folder.objectIds())
        new_obj = getattr(self.folder, auto_id)
    
        #Change the title
        obj_title = "New Title for Object"
        new_obj_path = '/%s' % new_obj.absolute_url(1)
        self.failUnless(new_obj.checkCreationFlag()) # object is not yet edited
    
        response = self.publish('%s/base_edit?form.submitted=1&title=%s&body=Blank' % (new_obj_path, obj_title,), self.basic_auth) # Edit object
        self.assertStatusEqual(response.getStatus(), 302) # OK
        self.failIf(new_obj.checkCreationFlag()) # object is fully created
        self.failUnlessEqual(new_obj.Title(),obj_title) # title is set
        self.failUnlessEqual(new_obj.getId(), auto_id) # id should not have changed
    
        del DDocument._at_rename_after_creation
    
    def test_id_change_with_without_marker(self):
        # Id should not be changed unless _at_rename_after_creation is set
        # on the class.
        # Make our content type use auto generated ids
        from Products.Archetypes.examples.DDocument import DDocument
        try:
            del DDocument._at_rename_after_creation
        except (AttributeError, KeyError):
            pass
    
        auto_id='orig_id'
    
        # create an object with an autogenerated id
        response = self.publish(self.folder_path +
                                '/invokeFactory?type_name=DDocument&id=%s'%auto_id,
                                self.basic_auth)
    
        # XXX now lets test if http://plone.org/collector/4487 is present
        if  "base_edit.cpt" in self.portal.portal_skins.archetypes.objectIds():
            raise AttributeError("test_id_change_with_without_marker is "
                  "expected to fail unless http://plone.org/collector/4487 is "
                  "fixed. This might also occur with chameleon cache files "
                  "but chameleon not installed. You can find them via: "
                  "find . -name \"*pt.py\"")
    
        self.failUnless(auto_id in self.folder.objectIds())
        new_obj = getattr(self.folder, auto_id)
    
        #Change the title
        obj_title = "New Title for Object"
        new_obj_path = '/%s' % new_obj.absolute_url(1)
        self.failUnless(new_obj.checkCreationFlag()) # object is not yet edited
    
        response = self.publish('%s/base_edit?form.submitted=1&title=%s&body=Blank' % (new_obj_path, obj_title,), self.basic_auth) # Edit object
        self.assertStatusEqual(response.getStatus(), 302) # OK
        self.failIf(new_obj.checkCreationFlag()) # object is fully created
        self.failUnlessEqual(new_obj.Title(),obj_title) # title is set
        self.failUnlessEqual(new_obj.getId(), auto_id) # id should not have changed

    def test_update_schema_does_not_reset_creation_flag(self):
        # This is functional so that we get a full request and set the flag

        # create an object with flag set
        response = self.publish(self.folder_path +
                              '/invokeFactory?type_name=DDocument&id=new_doc',
                              self.basic_auth)
        self.failUnless('new_doc' in self.folder.objectIds())
        new_obj = self.folder.new_doc
        self.failUnless(new_obj.checkCreationFlag()) # object is not yet edited
        obj_title = "New Title for Object"
        new_obj_path = '/%s' % new_obj.absolute_url(1)
        response = self.publish('%s/base_edit?form.submitted=1&title=%s&body=Blank' % (new_obj_path, obj_title,), self.basic_auth) # Edit object

        # now lets test if http://plone.org/collector/4487 is present
        if  "base_edit.cpt" in self.portal.portal_skins.archetypes.objectIds():
            raise AttributeError, ("test_update_schema_does_not_reset_creation_flag "
                  "is expected to fail unless  http://plone.org/collector/4487 is fixed")

        self.failIf(new_obj.checkCreationFlag()) # object is fully created
        # Now run the schema update
        req = self.app.REQUEST
        req.form['update_all']=True
        req.form['Archetypes.DDocument']=True
        self.portal.archetype_tool.manage_updateSchema(REQUEST=req)
        self.failIf(new_obj.checkCreationFlag())

    def test_createObjectViaWebDAV(self):
        # WebDAV upload should create new document without creation flag set
        response = self.publish(self.folder_path+'/new_html',
                                env={'CONTENT_TYPE': 'text/html'},
                                request_method='PUT',
                                stdin=StringIO(html),
                                basic=self.basic_auth)

        self.assertEqual(response.getStatus(), 201)
        self.failUnless('new_html' in self.folder.objectIds())
        self.assertEqual(self.folder.new_html.portal_type, 'DDocument')
        self.assertEqual(self.folder.new_html.getBody(), html)
        self.failIf(self.folder.new_html.checkCreationFlag())

    def test_createObjectInCodeDoesNotSetFlag(self):
        # Using invokeFactory from code should not set the creation flag

        # Functional sets the method to GET, this isn't really a functional
        # test but is a special case for the previous tests, so we'll unset
        # the REQUEST_METHOD.
        self.app.REQUEST.set('REQUEST_METHOD', 'nonsense')

        self.folder.invokeFactory('DDocument','bogus_item')
        self.failUnless('bogus_item' in self.folder.objectIds())
        self.failIf(self.folder.bogus_item.checkCreationFlag())

        self.app.REQUEST.set('REQUEST_METHOD','GET')


from zope.testing import doctest
OPTIONFLAGS = (doctest.ELLIPSIS |
               doctest.NORMALIZE_WHITESPACE)


def test_suite():
    from unittest import TestSuite, makeSuite
    from Testing.ZopeTestCase import FunctionalDocFileSuite as FileSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestFunctionalObjectCreation))
    testfiles = (
        'traversal_4981.txt',
        'folder_marshall.txt',
        'webdav_operations.txt',
        'traversal.txt',
        'reindex_sanity.txt',
    )
    for testfile in testfiles:
        suite.addTest(FileSuite(testfile, package="Products.Archetypes.tests",
                                optionflags=OPTIONFLAGS,
                                test_class=ATFunctionalSiteTestCase)
                     )
    return suite
