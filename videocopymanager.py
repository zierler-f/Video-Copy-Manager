#!/usr/bin/env python
import os, glob, sys

class VideoCopyManager(object):

    def __init__(self,source,target):
        self.source = source
        self.target = target

    def bothFoldersExist(self):
        if not os.path.isdir(self.source) or not os.path.isdir(self.target):
            raise TypeError('Either the provided source folder (' + self.source +
                            ') or the provided target folder (' + self.target +
                            ') does not exist in the file system.')
        return True

    def getFilesInFolder(self,path):
        files = []
        for root, subFolders, dirFiles in os.walk(path):
            for file in dirFiles:
                files.append(file)
        return files
