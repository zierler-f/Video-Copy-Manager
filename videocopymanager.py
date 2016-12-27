#!/usr/bin/env python
import mimetypes
import os
import re
import sys
from shutil import copyfile


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
        self.both_folders_exist()
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
                if filename_s == filename_t:
                    flag = True
            if not flag:
                missing_files.append(file_s)
        return missing_files

    def print_files_missing_in_target(self):
        for file in self.get_files_missing_in_target():
            print(file)

    def copy_missing_files_to_target(self):
        for file in self.get_files_missing_in_target():
            copyfile(file,os.path.join(self.target,os.path.basename(file)))

if __name__ == '__main__':
    if not len(sys.argv) == 4:
        raise TypeError("Please provide 3 arguments: videocopymanager.py <run_type> <source> <target>.")
    run_type = sys.argv[1]
    source = sys.argv[2]
    target = sys.argv[3]
    vcm = VideoCopyManager(source,target)
    if run_type == 'show':
        vcm.print_files_missing_in_target()
    elif run_type == 'cp':
        vcm.copy_missing_files_to_target()
    else:
        raise TypeError("Please use a valid argument for type. Valid arguments are 'show' and 'cp'!")
