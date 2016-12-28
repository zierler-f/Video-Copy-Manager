#!/usr/bin/env python

import io
import os
import sys
import tempfile
import unittest

import videocopymanager
from videocopymanager import VideoCopyManager


class TestVideoCopyManager(unittest.TestCase):
    source = tempfile.TemporaryDirectory()
    target = tempfile.TemporaryDirectory()
    ignore_file = tempfile.NamedTemporaryFile()
    f = open(ignore_file.name, "w")
    f.write("file7.mp4")
    f.close()
    vcm = VideoCopyManager(source.name, target.name, None, ignore_file.name)

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

        null_path = "/dev/null/file"
        tmp_file = tempfile.TemporaryFile()

        with self.assertRaises(TypeError):
            VideoCopyManager(null_path, self.target.name, None, None)
        with self.assertRaises(TypeError):
            VideoCopyManager(self.source.name, null_path, None, None)
        with self.assertRaises(TypeError):
            VideoCopyManager(null_path, null_path, None, None)
        with self.assertRaises(TypeError):
            VideoCopyManager(self.source.name, tmp_file.name, None, None)
        with self.assertRaises(TypeError):
            VideoCopyManager(tmp_file.name, self.target.name, None, None)

    def test_get_files_in_folder(self):
        """
        Assert 5 created files are found in TemporaryFolder
        :return:
        """
        tmp_dir = tempfile.TemporaryDirectory()
        file1 = os.path.join(tmp_dir.name, "file")
        dir1 = os.path.join(tmp_dir.name, "dir")
        file2 = os.path.join(dir1, "file")
        file3 = os.path.join(dir1, "file1")
        dir2 = os.path.join(dir1, "dir")
        file4 = os.path.join(dir2, "file")
        file5 = os.path.join(dir2, "file1")
        open(file1, "wb")
        os.mkdir(dir1)
        open(file2, "wb")
        open(file3, "wb")
        os.mkdir(dir2)
        open(file4, "wb")
        open(file5, "wb")
        result = videocopymanager.get_files_in_folder_recursive(tmp_dir.name)
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
        file1 = os.path.join(tmp_dir.name, "file.mp4")
        dir1 = os.path.join(tmp_dir.name, "dir")
        file2 = os.path.join(dir1, "file")
        file3 = os.path.join(dir1, "file.mkv")
        dir2 = os.path.join(dir1, "dir")
        file4 = os.path.join(dir2, "file")
        file5 = os.path.join(dir2, "file.flv")
        open(file1, "wb")
        os.mkdir(dir1)
        open(file2, "wb")
        open(file3, "wb")
        os.mkdir(dir2)
        open(file4, "wb")
        open(file5, "wb")
        result = videocopymanager.get_video_files_in_folder_recursive(tmp_dir.name)
        self.assertEqual(3, len(result))
        self.assertTrue(result.__contains__(file1))
        self.assertTrue(result.__contains__(file3))
        self.assertTrue(result.__contains__(file5))

    def test_get_files_missing_in_target(self):
        """
        Create files in source and target and make sure missing files are correct
        :return:
        """

        source = tempfile.TemporaryDirectory()
        target = tempfile.TemporaryDirectory()
        ignore_file = tempfile.NamedTemporaryFile()
        f = open(ignore_file.name, "w")
        f.write("file7.mp4")
        f.close()
        vcm = VideoCopyManager(source.name, target.name, None, ignore_file.name)

        file1_src = os.path.join(source.name, "file1.mp4")
        file1_tgt = os.path.join(target.name, "file1.mp4")
        file2_src = os.path.join(source.name, "file2.mp4")
        dir1_src = os.path.join(source.name, "dir1_src")
        dir1_tgt = os.path.join(target.name, "dir1_tgt")
        file3_src = os.path.join(dir1_src, "file3.mp4")
        file4_tgt = os.path.join(dir1_tgt, "file4.mp4")
        file5_src = os.path.join(dir1_src, "file5.mp4")
        file5_tgt = os.path.join(dir1_tgt, "file5.mp4")
        dir2_src = os.path.join(dir1_src, "dir2_src")
        dir2_tgt = os.path.join(dir1_tgt, "dir2_tgt")
        file3_tgt = os.path.join(dir2_tgt, "file3.mp4")
        file6_src = os.path.join(dir2_src, "file6.mp4")
        file7_src = os.path.join(dir2_src, "file7.mp4")

        open(file1_src, "wb")
        open(file1_tgt, "wb")
        open(file2_src, "wb")
        os.mkdir(dir1_src)
        os.mkdir(dir1_tgt)
        open(file3_src, "wb")
        open(file4_tgt, "wb")
        open(file5_src, "wb")
        open(file5_tgt, "wb")
        os.mkdir(dir2_src)
        os.mkdir(dir2_tgt)
        open(file3_tgt, "wb")
        open(file6_src, "wb")
        open(file7_src, "wb")

        result = vcm.get_files_missing_in_target()
        self.assertEqual(2, len(result))
        self.assertTrue(result.__contains__(file2_src))
        self.assertTrue(result.__contains__(file6_src))

    def test_videocopymanager_main(self):
        with self.assertRaises(TypeError):
            videocopymanager.main("Test")
        with self.assertRaises(TypeError):
            videocopymanager.main(["test", "test"])
        with self.assertRaises(TypeError):
            videocopymanager.main(["test", "test", "test", "test"])
        with self.assertRaises(TypeError):
            videocopymanager.main(["test", "test", "test", "test", "test", "test"])
        source = tempfile.TemporaryDirectory()
        target = tempfile.TemporaryDirectory()
        cp_target = os.path.join(target.name, "cp_tgt")
        os.mkdir(cp_target)
        ignore_file = tempfile.NamedTemporaryFile()
        f = open(ignore_file.name, "w")
        f.write("file2.mp4")
        f.close()
        file1_src = os.path.join(source.name, "file1.mp4")
        file1_tgt = os.path.join(target.name, "file1.mp4")
        file2_src = os.path.join(source.name, "file2.mp4")
        file3_src = os.path.join(source.name, "file3.mp4")
        open(file1_src, "wb")
        open(file1_tgt, "wb")
        open(file2_src, "wb")
        open(file3_src, "wb")
        out = io.StringIO()
        sys.stdout = out
        videocopymanager.main(["show", source.name, target.name, cp_target, ignore_file.name])
        file3_basename = os.path.basename(file3_src)
        expected_out = file3_basename
        self.assertEqual(expected_out, out.getvalue().strip())
        videocopymanager.main(["cp", source.name, target.name, cp_target, ignore_file.name])
        videocopymanager.main(["show", source.name, target.name, cp_target, ignore_file.name])
        expected_out += "\nNow copying " + file3_basename + ".\n" + \
                        "Successfully copied " + file3_basename + "."
        self.assertEqual(expected_out, out.getvalue().strip())
