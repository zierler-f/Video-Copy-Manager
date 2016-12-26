#!/usr/bin/env python
import os

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
