#!/usr/bin/env python
import mimetypes
import os
import re


def is_video_file(type):
    try:
        return re.search("video\/.*", type);
    except TypeError:
        return False


class VideoCopyManager(object):
    def __init__(self, source, target):
        self.source = source
        self.target = target
        mimetypes.init()

    def both_folders_exist(self):
        if not os.path.isdir(self.source) or not os.path.isdir(self.target):
            raise TypeError('Either the provided source folder (' + self.source +
                            ') or the provided target folder (' + self.target +
                            ') does not exist in the file system.')
        return True

    def get_files_in_folder_recursive(self, path):
        files = []
        for root, subFolders, dirFiles in os.walk(path):
            for file in dirFiles:
                filepath = os.path.join(root, file)
                files.append(filepath)
        return files

    def get_video_files_in_folder_recursive(self, path):
        files = []
        for file in self.get_files_in_folder_recursive(path):
            type = mimetypes.guess_type(file)[0]
            if is_video_file(type):
                files.append(file)
        return files
