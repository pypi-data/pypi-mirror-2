# -*- encoding: UTF-8 -*-
'''
Created on 5 avr. 2010

@author: thierry
'''

import os.path
import hashlib
import webbrowser

import storage

from caritang.common import version 

version.getInstance().submitRevision("$Revision: 67 $")

SAVED_SUCCESS = 0
SAVED_ALREADY = 1
SAVED_FAILURE = 2

CONNECT_SUCCESS = 0
CONNECT_FAILURE = 1

class ProgressListener(object):
    '''
    Interface for progress listener
    '''
    def startSaveDocItem(self, docItem):
         raise RuntimeError(NOT_YET_IMPLEMENTED)
    
    def endSaveDocItem(self, docItem, storage, status):
         raise RuntimeError(NOT_YET_IMPLEMENTED)
     
    def handleCaptcha(self, url, storage):
        raise RuntimeError(NOT_YET_IMPLEMENTED)   
    
    def connectToStorage(self, storgae, status):
        raise RuntimeError(NOT_YET_IMPLEMENTED)          
       
class NoOpProgressListener(ProgressListener):

    def handleCaptcha(self, token, storage):
        return ProgressListener.handleCaptcha(self, token, storage)


    def connectToStorage(self, storgae, status):
        return ProgressListener.connectToStorage(self, storgae, status)


    def handleCaptcha(self, url, storage):
        pass


    def connectToStorage(self, storage, status):
        pass


    def startSaveDocItem(self, docItem):
        pass


    def endSaveDocItem(self, docItem, storage, status):
        pass

class verboseProgressListener(ProgressListener):

    def handleCaptcha(self, url, storage):
        print storage.getName() + " requires captcha validation"
        print "Please visite the site " + url
        webbrowser.open_new_tab(url)
        response = raw_input("Type the captcha image here:")
        return response 


    def connectToStorage(self, storage, status):
        if status == CONNECT_SUCCESS:
            print "connected to " + storage.getName()
        else:
            print "failed to connect to " + storage.getName()


    def startSaveDocItem(self, docItem):
        print "saving " + docItem.getFile() + " ...."



    def endSaveDocItem(self, docItem, storage, status):
        if status == SAVED_SUCCESS:
            print "ok in " + str(storage)
        elif status == SAVED_ALREADY:
            print "skipped for " + str(storage)
        else : 
            print "FAILED in " + str(storage)

    pass

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

    def _ensure_storage_is_connected(self, progress_listener, a_storage):
        while not a_storage.isConnected():
            try:
                a_storage.connect()
            except storage.CaritangCaptchaException, e:
                response = progress_listener.handleCaptcha(e.get_url(), e.get_storage())
                e.get_storage().connect(e.get_token(), response)
            
            if a_storage.isConnected():
                progress_listener.connectToStorage(a_storage, CONNECT_SUCCESS)
            else:
                progress_listener.connectToStorage(a_storage, CONNECT_FAILURE)        


    def _get_caritang_storage_dir(self):
        '''
        Compute the file  system storage for caritang stuff
        '''
        storage = os.path.expanduser("~")
        storage = os.path.join(storage, ".caritang")
        return storage   
    
    def _get_storage_home(self, a_storage):
        storage = os.path.join(self._get_caritang_storage_dir(), a_storage.getName())
        return storage


    def _ensure_storage_home_exist(self, a_storage):
        storage = self._get_storage_home(a_storage)
        if not os.path.exists(storage):
            os.makedirs(storage)        
        return storage

            
    
    def addSource(self, aSource):
        self.sources.append(aSource) 
        
    def addStorage(self, aStorage):
        self.storages.append(aStorage)
    
    
    def save(self, resume=True, progress_listener=NoOpProgressListener()):
        '''
        save all source data to each storage. The default parameter resume is valued
        to True so the archiver attemps to resume the backup e.g. backup only new file.
        '''
        
        # ensure storage home exist for each storage
        for a_storage in self.storages:
            self._ensure_storage_home_exist(a_storage)
            
       
        for a_source in self.sources :
            for doc in a_source.list_document() :
                progress_listener.startSaveDocItem(doc)
                for a_storage in self.storages :                                        
                    # check if the doc hasnot already been saved by this storage
                    if resume == False or not self._isMarkedAsSaved(doc, a_storage):
                        self._ensure_storage_is_connected(progress_listener, a_storage)
                        try :                                                                                                 
                            a_storage.store(doc)
                        except storage.CaritangStorageException, e:                        
                            progress_listener.endSaveDocItem(doc, a_storage, SAVED_FAILURE)
                        else:
                            # mark the doc as saved
                            self._markAsSaved(doc,a_storage)
                            progress_listener.endSaveDocItem(doc, a_storage, SAVED_SUCCESS)
                    else :
                        progress_listener.endSaveDocItem(doc, a_storage, SAVED_ALREADY)
                        
        
    
    
    def _isMarkedAsSaved(self,  a_docItem, a_storage):
        '''
        Test is a foc item has already been saved.
        '''
        storage = self._get_storage_home(a_storage)
        
        digest = self._computeDigestForDocItem(a_docItem)
        
        savedMarkup = os.path.join(storage, digest)
        
        return os.path.exists(savedMarkup)
      
    def _computeDigestForDocItem(self, a_docItem):   
        md5 = hashlib.md5(a_docItem.getFile())       
        digest = md5.hexdigest()
        return digest  
        
    def _markAsSaved(self,a_docItem, a_storage):
        '''
        Mark a docItem as saved.
        Further call to save with resume=True will not save the docItem again
        ''' 
        storage = self._get_storage_home(a_storage)
        
        digest = self._computeDigestForDocItem(a_docItem)
        
        savedMarkup = os.path.join(storage, digest)
        f = open(savedMarkup,"w")
        f.close()
        