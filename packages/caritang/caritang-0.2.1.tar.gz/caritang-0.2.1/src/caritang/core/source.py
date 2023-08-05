# -*- encoding: UTF-8 -*-
'''
Created on 5 avr. 2010

@author: thierry
'''

import os.path

from caritang.common import version 

version.getInstance().submitRevision("$Revision: 33 $")


NOT_YET_IMPLEMENTED = "not yet implemented"

class DocSource(object):
    '''
    Interace for any document source. A document source may content many elements.
    '''
    
    def list_document(self):
        '''
        list all document from this source.
        Return an interator on DocItem
        '''
        raise RuntimeError(NOT_YET_IMPLEMENTED)

class DocItem(object):
    '''
    Interface for a document item
    '''
    
    def getName(self):
        '''
        Return the name of the document
        '''
        raise RuntimeError(NOT_YET_IMPLEMENTED)
    
    def getFile(self):
        '''
        Return the file url
        '''
        raise RuntimeError(NOT_YET_IMPLEMENTED)
    

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
                del dirs[:]
            for file in files :
                yield FileDocItem(os.path.join(root, file))

class FileDocItem(DocItem):
    
    def __init__(self, filepath):
        self.filepath = filepath

    def getName(self):
        return os.path.basename(self.filepath)


    def getFile(self):
        return self.filepath
        
            