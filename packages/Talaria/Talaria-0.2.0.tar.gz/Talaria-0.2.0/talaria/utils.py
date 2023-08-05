# -*- coding: utf-8 -*-
import os
from fnmatch import fnmatch
from mercurial import util, commands, ui, hg

__all__ = 'HgPath DescriptiveString'.split()

class HgPath(object):

    def __init__(self, changectx):
        self.changectx = changectx
        self.files = changectx.manifest().keys()
        self.directories = set([''])
        for f in self.files:
            d = os.path.dirname(f)
            while d != '':
                self.directories.add(d)
                d = os.path.dirname(d)
        self.directories = list(self.directories)
        self.files.sort()
        self.directories.sort()

    def exists(self, path):
        path = path.rstrip('/')
        return self.isdir(path) | self.isfile(path)

    def isdir(self, path):
        path = path.rstrip('/')
        return path in self.directories

    def isfile(self, path):
        path = path.rstrip('/')
        return path in self.files

    def listdir(self, path):
        path = path.rstrip('/')
        ret = []
        for item in self.files + self.directories:
            parent = os.path.dirname(item)
            if parent != item and parent == path:
                ret.append(os.path.basename(item))
        ret.sort()
        return ret

    def glob(self, dirname, pattern):
        """ works in hg repo as glob.glob1 for files """
        ret = [ f for f in self.listdir(dirname) if fnmatch(f, pattern) ]
        ret.sort()
        return ret

    def data(self, path):
        path = path.rstrip('/')
        if self.isfile(path):
            return self.changectx.filectx(path).data()
        raise IOError('File %s does not exist' % str(path))


class DescriptiveString(unicode): pass
