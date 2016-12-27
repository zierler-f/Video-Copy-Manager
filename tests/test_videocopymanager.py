#!/usr/bin/env python

import unittest, tempfile, os
from videocopymanager import VideoCopyManager

class TestVideoCopyManager(unittest.TestCase):

    source = tempfile.TemporaryDirectory()
    target = tempfile.TemporaryDirectory()
    vcm = VideoCopyManager(source.name,target.name)

    def test_video_copy_manager_creation(self):
        """
        Make sure Video Copy Manager is imported
        """
        assert self.vcm is not None

    def test_both_folders_exist(self):
        """
        Make sure the project is only run when both folders exist
        """
        self.assertTrue(self.vcm.both_folders_exist())

        nullPath = "/dev/null/file"
        tmpFile = tempfile.TemporaryFile()

        vcm = VideoCopyManager(nullPath,self.target.name)
        with self.assertRaises(TypeError):
            vcm.both_folders_exist()

        vcm = VideoCopyManager(self.source.name,nullPath)
        with self.assertRaises(TypeError):
            vcm.both_folders_exist()

        vcm = VideoCopyManager(nullPath,nullPath)
        with self.assertRaises(TypeError):
            vcm.both_folders_exist()

        vcm = VideoCopyManager(self.source.name,tmpFile.name)
        with self.assertRaises(TypeError):
            vcm.both_folders_exist()

        vcm = VideoCopyManager(tmpFile.name,self.target.name)
        with self.assertRaises(TypeError):
            vcm.both_folders_exist()

    def test_get_files_in_folder(self):
        """
        Assert 5 created files are found in TemporaryFolder
        :return:
        """
        tmp_dir = tempfile.TemporaryDirectory()
        file1 = os.path.join(tmp_dir.name,"file")
        dir1 = os.path.join(tmp_dir.name,"dir")
        file2 = os.path.join(dir1,"file")
        file3 = os.path.join(dir1,"file1")
        dir2 = os.path.join(dir1,"dir")
        file4 = os.path.join(dir2,"file")
        file5 = os.path.join(dir2,"file1")
        open(file1, 'wb')
        os.mkdir(dir1)
        open(file2, 'wb')
        open(file3, 'wb')
        os.mkdir(dir2)
        open(file4, 'wb')
        open(file5, 'wb')
        result = self.vcm.get_files_in_folder_recursive(tmp_dir.name)
        self.assertEqual(5, len(result))
        self.assertTrue(result.__contains__(file1))
        self.assertTrue(result.__contains__(file2))
        self.assertTrue(result.__contains__(file3))
        self.assertTrue(result.__contains__(file4))
        self.assertTrue(result.__contains__(file5))

    def test_get_video_files_in_folder(self):
        """
        Assert 3 created video files are found in TemporaryFolder and non-video files are not found
        :return:
        """
        tmp_dir = tempfile.TemporaryDirectory()
        file1 = os.path.join(tmp_dir.name,"file.mp4")
        dir1 = os.path.join(tmp_dir.name,"dir")
        file2 = os.path.join(dir1,"file")
        file3 = os.path.join(dir1,"file.mkv")
        dir2 = os.path.join(dir1,"dir")
        file4 = os.path.join(dir2,"file")
        file5 = os.path.join(dir2,"file.flv")
        open(file1, 'wb')
        os.mkdir(dir1)
        open(file2, 'wb')
        open(file3, 'wb')
        os.mkdir(dir2)
        open(file4, 'wb')
        open(file5, 'wb')
        result = self.vcm.get_video_files_in_folder_recursive(tmp_dir.name)
        self.assertEqual(3, len(result))
        self.assertTrue(result.__contains__(file1))
        self.assertTrue(result.__contains__(file3))
        self.assertTrue(result.__contains__(file5))

