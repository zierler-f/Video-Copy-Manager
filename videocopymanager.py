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
    def __init__(self, source, target, cp_target, ignore_file):
        self.source = source
        self.target = target
        self.both_folders_exist()
        if cp_target is None:
            self.cp_target = target
        else:
            self.cp_target = cp_target
        self.ignore_file = ignore_file
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
        ignore_filenames = self.get_ignore_filenames()
        missing_files = []
        for file_s in files_source:
            flag = False
            filename_s = os.path.basename(file_s)
            for file_t in files_target:
                filename_t = os.path.basename(file_t)
                if filename_s == filename_t:
                    flag = True
            if not flag and not ignore_filenames.__contains__(filename_s):
                missing_files.append(file_s)
        return missing_files

    def get_ignore_filenames(self):
        ignore_filenames = []
        if self.ignore_file is not None:
            if os.path.isfile(self.ignore_file):
                with open(self.ignore_file) as f:
                    for line in f:
                        ignore_filenames.append(line)
        return ignore_filenames

    def print_files_missing_in_target(self):
        for file in self.get_files_missing_in_target():
            print(file)

    def copy_missing_files_to_target(self):
        for file in self.get_files_missing_in_target():
            cp_target = self.cp_target
            if not os.path.isdir(cp_target):
                print(cp_target + " not found. Now using target (" + self.target + ") instead.")
                cp_target = target
            print('Now copying ' + file + ".")
            copyfile(file, os.path.join(cp_target, os.path.basename(file)))
            print('Successfully copied ' + file + ".")


if __name__ == '__main__':
    args_len = len(sys.argv)
    if args_len == 4 or args_len == 6:
        run_type = sys.argv[1]
        source = sys.argv[2]
        target = sys.argv[3]
        cp_target = None
        ignore_file = None
        if args_len == 6:
            cp_target = sys.argv[4]
            ignore_file = sys.argv[5]
        vcm = VideoCopyManager(source, target, cp_target, ignore_file)
        if run_type == 'show':
            vcm.print_files_missing_in_target()
        elif run_type == 'cp':
            vcm.copy_missing_files_to_target()
        else:
            raise TypeError("Please use a valid argument for type. Valid arguments are 'show' and 'cp'!")
    else:
        raise TypeError(
            "Please provide 3 - 5 arguments: videocopymanager.py <run_type> <source> <target> [<copy-target>] [<ignorefile>].")
