#!/usr/bin/env python
import os, magic

class VideoCopyManager(object):

    def __init__(self,source,target):
        self.source = source
        self.target = target

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
                filepath = os.path.join(root,file)
                files.append(filepath)
        return files

    def get_video_files_in_folder_recursive(self,path):
        files = []
        for file in self.get_files_in_folder_recursive(path):
            mime = magic.Magic(mime=True)
            mimetype = mime.from_file(filename=file)
            filetype = mimetype.split("/")[0]
            if filetype is "video":
                files.append(file)
        return files
