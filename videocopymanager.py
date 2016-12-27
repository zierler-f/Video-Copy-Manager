#!/usr/bin/env python
import mimetypes
import os
import re


def is_video_file(type):
    try:
        return re.search("video\/.*", type);
    except TypeError:
        return False


def get_files_in_folder_recursive(path):
    files = []
    for root, subFolders, dirFiles in os.walk(path):
        for file in dirFiles:
            filepath = os.path.join(root, file)
            files.append(filepath)
    return files


def get_video_files_in_folder_recursive(path):
    files = []
    for file in get_files_in_folder_recursive(path):
        type = mimetypes.guess_type(file)[0]
        if is_video_file(type):
            files.append(file)
    return files


class VideoCopyManager:
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

    def get_files_missing_in_target(self):
        files_source = get_video_files_in_folder_recursive(self.source)
        files_target = get_video_files_in_folder_recursive(self.target)
        missing_files = []
        for file_s in files_source:
            flag = False
            filename_s = os.path.basename(file_s)
            for file_t in files_target:
                filename_t = os.path.basename(file_t)
                if filename_s is filename_t:
                    flag = True
            if not flag:
                missing_files.append(file_s)
        return missing_files