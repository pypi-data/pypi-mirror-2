import unittest
import dm.times
import dm.dictionary
from dm.dictionarywords import *
import os

def suite():
    suites = [
        unittest.makeSuite(TestSystemDictionary),
    ]
    return unittest.TestSuite(suites)


class TestSystemDictionary(unittest.TestCase):

    def setUp(self):
        self.dictionary = dm.dictionary.SystemDictionary()

    def test_systemName(self):
        self.failUnlessEqual(self.dictionary[SYSTEM_NAME], 'domainmodel')
        if self.dictionary[IMAGES_DIR_PATH]:
            imagesPath = self.dictionary[IMAGES_DIR_PATH]
            self.failUnless(os.path.exists(imagesPath), imagesPath)

    def test_systemUserName(self):
        self.failUnlessEqual(self.dictionary[SYSTEM_USER_NAME], os.environ['USER'])

    def test_systemUpSince(self):
        upSince = self.dictionary[SYSTEM_UP_SINCE]
        self.failUnless(upSince)
        self.failUnless(upSince < dm.times.getUniversalNow())

