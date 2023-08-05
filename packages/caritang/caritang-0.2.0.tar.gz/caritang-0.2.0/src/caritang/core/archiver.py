# -*- encoding: UTF-8 -*-
'''
Created on 5 avr. 2010

@author: thierry
'''

import storage

from caritang.common import version 

version.getInstance().submitRevision("$Revision: 24 $")

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
        self.progress_listener = None
            
    
    def addSource(self, aSource):
        self.sources.append(aSource) 
        
    def addStorage(self, aStorage):
        self.storages.append(aStorage)
        
    def save(self, resume=True):
        '''
        save all source data to each storage. The default parameter resume is valued
        to True so the archiver attemps to resume the backup e.g. backup only new file.
        '''
        for a_source in self.sources :
            for doc in a_source.list_document() :
                for a_storage in self.storages :
                    try :
                        a_storage.store(doc)
                    except storage.CaritangStorageException, e:
                        if self.progress_listener is not None:
                            self.progress_listener.receive_signal(e)
                    