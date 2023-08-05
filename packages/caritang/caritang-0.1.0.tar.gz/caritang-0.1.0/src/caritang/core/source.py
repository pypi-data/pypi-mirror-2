# -*- encoding: UTF-8 -*-
'''
Created on 5 avr. 2010

@author: thierry
'''

import os.path

from caritang.common import version 

version.getInstance().submitRevision("$Revision: 2 $")


NOT_YET_IMPLEMENTED = "not yet implemented"

class DocSource(object):
    '''
    Interace for any document source
    '''
    

class Directory(DocSource):
    '''
    Local directory to backup.
    '''


    def __init__(self, directory, recursive=True, filter=None):
        '''
        Constructor
        '''
        self.directory = directory
        self.recursive = recursive
        self.filter = filter

    def list_document(self):
        for root, dirs, files in os.walk(self.directory) :
            if not self.recursive:
                dirs.clear()
            for file in files :
                yield os.path.join(root, file)

    
            