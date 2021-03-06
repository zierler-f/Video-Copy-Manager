#!/usr/bin/env python
import mimetypes
import os
import re
import sys
from shutil import copyfile


def main(args):
    if type(args) is not list:
        raise TypeError("Args were not of type list.")
    args_len = len(args)
    if args_len == 3 or args_len == 5:
        run_type = args[0]
        source = args[1]
        target = args[2]
        cp_target = None
        ignore_file = None
        if args_len == 5:
            cp_target = args[3]
            ignore_file = args[4]
        vcm = VideoCopyManager(source, target, cp_target, ignore_file)
        if run_type == "show":
            vcm.print_files_missing_in_target()
        elif run_type == "cp":
            vcm.copy_missing_files_to_target()
        elif run_type == "ln":
            vcm.link_missing_files_to_target()
        else:
            raise TypeError("Please use a valid argument for type. Valid arguments are 'show' and 'cp'!")
    else:
        raise TypeError("Please provide 3 - 5 arguments:"
                        " videocopymanager.py <run_type> <source> <target> [<copy-target>] [<ignorefile>].")


def is_video_file(mimetype):
    try:
        return re.search("video/.*", mimetype)
    except TypeError:
        return False


def get_files_in_folder_recursive(path):
    files = []
    for root, sub_folders, dir_files in os.walk(path):
        for file in dir_files:
            filepath = os.path.join(root, file)
            files.append(filepath)
    return files


def get_video_files_in_folder_recursive(path):
    files = []
    for file in get_files_in_folder_recursive(path):
        mimetype = mimetypes.guess_type(file)[0]
        if is_video_file(mimetype):
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
            raise TypeError("Either the provided source folder (" + self.source +
                            ") or the provided target folder (" + self.target +
                            ") does not exist in the file system.")
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
        if self.ignore_file is not None and os.path.isfile(self.ignore_file):
            f = open(self.ignore_file)
            return f.read().splitlines()
        return []

    def print_files_missing_in_target(self):
        for file in self.get_files_missing_in_target():
            print(os.path.basename(file))

    def copy_missing_files_to_target(self):
        for file in self.get_files_missing_in_target():
            cp_target = self.cp_target
            if not os.path.isdir(cp_target):
                print(cp_target + " not found. Now using target (" + self.target + ") instead.")
                cp_target = self.target
            file_basename = os.path.basename(file)
            print("Now copying " + file_basename + ".")
            copyfile(file, os.path.join(cp_target, file_basename))
            print("Successfully copied " + file_basename + ".")

    def link_missing_files_to_target(self):
        for file in self.get_files_missing_in_target():
            cp_target = self.cp_target
            if not os.path.isdir(cp_target):
                print(cp_target + " not found. Now using target (" + self.target + ") instead.")
                cp_target = self.target
            file_basename = os.path.basename(file)
            print("Now linking " + file_basename + ".")
            os.link(file, os.path.join(cp_target, file_basename))
            print("Successfully linked " + file_basename + ".")


if __name__ == "__main__":
    sys.argv.pop(0)
    main(sys.argv)
