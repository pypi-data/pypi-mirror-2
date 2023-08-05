# -*- encoding: UTF-8 -*-
'''
Created on 5 avr. 2010

@author: thierry
'''

from caritang.common import version 

version.getInstance().submitRevision("$Revision: 2 $")

class Archiver(object):
    '''
    This class is responsible for upload documents to google docs account.
    '''


    def __init__(self):
        '''
        Constructor
        '''
        self.sources = []
        self.storages = []
            
    
    def addSource(self, aSource):
        self.sources.append(aSource) 
        
    def addStorage(self, aStorage):
        self.storages.append(aStorage)
        
    def save(self, resume=True):
        '''
        save all source data to each storage. The default parameter resume is valued
        to True so the archiver attemps to resume the backup e.g. backup only new file.
        '''
        for source in self.sources :
            for doc in source.list_document() :
                for storage in self.storages :
                    storage.store(doc)
                    