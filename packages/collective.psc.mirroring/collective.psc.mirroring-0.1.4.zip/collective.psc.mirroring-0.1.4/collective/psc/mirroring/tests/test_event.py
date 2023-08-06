import unittest
import os
import shutil
from os.path import join

from zope.testing import doctestunit
from zope.component import testing
from zope.component import getUtility
from Testing import ZopeTestCase as ztc

from Products.Five import zcml
from Products.Five import fiveconfigure
from Products.PloneTestCase import PloneTestCase as ptc
from Products.PloneTestCase.layer import PloneSite
from Products.PloneSoftwareCenter.tests import base
from ZODB.POSException import ConflictError 

from zope.formlib import form
from zope.event import notify
from zope.publisher.browser import TestRequest

from Products.CMFCore.utils import getToolByName

from collective.psc.mirroring.interfaces import IFSMirrorConfiguration
import collective.psc.mirroring

ptc.setupPloneSite(products=["collective.psc.mirroring", 
                             "Products.PloneSoftwareCenter"])

class TestCase(ptc.PloneTestCase):
    class layer(PloneSite):
        @classmethod
        def setUp(cls):
            PloneSite.setUp()
            fiveconfigure.debug_mode = True
            zcml.load_config('configure.zcml',
                             collective.psc.mirroring)
            fiveconfigure.debug_mode = False
            ztc.installPackage('collective.psc.mirroring')

        @classmethod
        def tearDown(cls):
            PloneSite.tearDown()

    def afterSetUp(self):
        
        self.setRoles(('Manager',))
        self.portal.invokeFactory('PloneSoftwareCenter', 'psc')
        self.portal.psc.invokeFactory('PSCProject', 'proj')
        self.psc = self.portal.psc
        self.proj = self.portal.psc.proj
        self.wf = getToolByName(self.proj, 'portal_workflow')
        self.proj.invokeFactory('PSCReleaseFolder', 'relfolder')
        self.proj.relfolder.invokeFactory('PSCRelease', 'rel') 
        self.proj.relfolder.rel.invokeFactory('PSCFile', 'file')
        self.file_path = join(os.path.dirname(__file__), 'files')
        if not os.path.exists(self.file_path):
            os.mkdir(self.file_path)

        config = IFSMirrorConfiguration(self.portal)
        mirror_form = form.Fields(IFSMirrorConfiguration)
        mirror_form.get("path").field.set(config, unicode(self.file_path))

    def tearDown(self):
        shutil.rmtree(self.file_path)

    def test_copied(self):
        # let's publish a release
        rel = self.proj.relfolder.rel 

        self.wf.doActionFor(rel, 'release-alpha') 
       
        # we should have a file now in the folder
        contents = os.listdir(self.file_path)
        contents.sort()
        self.assertEquals(contents, ['file', 'index'])
        
        # let's check the index file
        content = open(join(self.file_path, 'index')).readlines()
        content = content[0].split('#')
        self.assertEquals(content[1].strip(), 'd41d8cd98f00b204e9800998ecf8427e')

        # now let's hide it
        self.wf.doActionFor(rel, 'retract')

        # the file should be removed
        contents = os.listdir(self.file_path)
        self.assertEquals(contents, ['index'])

    def _test_lock(self):
        # let's lock the file
        from collective.psc.mirroring.locker import with_lock
        filename = join(self.file_path, 'file')

        def locked_state(file_):
            # let's try to notify here, we should get a conflict error
            self.proj.relfolder.rel.file.update_data('xx')
            wf.doActionFor(rel, 'release-beta')
            self.assertRaises(ConflictError, notify, edited)  
        
        with_lock(filename, 'wb', locked_state)

    def test_same_file_exists(self):
        # we want to avoid copying a file that is already there
        # using MD5 keys
        pass

    def test_file_removed(self):
        root = getUtility(IFSMirrorConfiguration).path
        self.assertEquals(root, self.file_path)

        rel = self.proj.relfolder.rel

        # let's release
        self.wf.doActionFor(rel, 'release-alpha')
        
        # let's check we have a file
        contents = os.listdir(self.file_path)
        self.assertEquals(contents, ['file', 'index'])

        # we have a file, in a published release, let's remove it !
        rel.manage_delObjects(['file'])

        # let's check the file has been removed
        contents = os.listdir(self.file_path)
        self.assertEquals(contents, ['index'])

        # let's add a file
        f = rel.invokeFactory('PSCFile', 'file')
        
        # let's check we have a file
        contents = os.listdir(self.file_path)
        self.assertEquals(contents, ['file', 'index'])
        

def test_suite():
    return unittest.TestSuite((unittest.makeSuite(TestCase),))


if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
