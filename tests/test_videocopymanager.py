#!/usr/bin/env python

import unittest, tempfile, os
from videocopymanager import VideoCopyManager

class TestVideoCopyManager(unittest.TestCase):

    source = tempfile.TemporaryDirectory()
    target = tempfile.TemporaryDirectory()
    vcm = VideoCopyManager(source.name,target.name)

    def testVideoCopyManagerCreation(self):
        """
        Make sure Video Copy Manager is imported
        """
        assert self.vcm is not None

    def testBothFoldersExist(self):
        """
        Make sure the project is only run when both folders exist
        """
        self.assertTrue(self.vcm.bothFoldersExist())

        nullPath = "/dev/null/file"
        tmpFile = tempfile.TemporaryFile()

        vcm = VideoCopyManager(nullPath,self.target.name)
        with self.assertRaises(TypeError):
            vcm.bothFoldersExist()

        vcm = VideoCopyManager(self.source.name,nullPath)
        with self.assertRaises(TypeError):
            vcm.bothFoldersExist()

        vcm = VideoCopyManager(nullPath,nullPath)
        with self.assertRaises(TypeError):
            vcm.bothFoldersExist()

        vcm = VideoCopyManager(self.source.name,tmpFile.name)
        with self.assertRaises(TypeError):
            vcm.bothFoldersExist()

        vcm = VideoCopyManager(tmpFile.name,self.target.name)
        with self.assertRaises(TypeError):
            vcm.bothFoldersExist()

    def testGetFilesInFolder(self):
        """
        Assert 5 created files are found in TemporaryFolder
        :return:
        """
        for i in range(5):
            open(os.path.join(self.source.name,str(i)), 'wb')
        self.assertEqual(5,len(self.vcm.getFilesInFolder(self.source.name)))
