# -*- encoding: UTF-8 -*-
'''
Created on Apr 18, 2010

@author: maemo
'''

import sys, os

import archiver
import source
import storage

from ..common import version 

version.getInstance().submitRevision("$Revision: 33 $")

def replace_special_character(a_string):
    return a_string.replace("/","_").replace(".","") # to be modified if needed

class Caritang(object):
    '''
    classdocs
    '''

    @classmethod
    def getN900DefaultInstance(cls, login, password):
        '''
        create a caritang instance configured to save most important N900 directories.
        The directories are
        ~/MyDocs/.documents
        ~/MyDocs/DCIM
        '''
        home = os.path.expanduser("~")
        mydocs = os.path.join(home,"MyDocs")
        documents = os.path.join(mydocs,".documents")
        dcim = os.path.join(mydocs,"DCIM")
        return Caritang(login, password,"N900",False,True,True,dcim, documents)

    def __init__(self, login, password, folder, remove, flatten, verbose, *dirs):
        '''
        Constructor
        '''
        self.login = login
        self.password = password
        self.folder = folder
        self.remove = remove
        self.flatten = flatten
        self.verbose = verbose
        self.dirs = dirs
        
    
    def save(self,progressListener=None):       
        if self.flatten :
            for dir in self.dirs:                
                # generate as many remote directory as subfolder in local directory
                for root, dir_list, files in os.walk(dir) :                   
                    folder_name = self.folder
                    extra = root.partition(dir)[2] # part after dir
                    if len(extra) > 0 :
                        if folder_name is None:
                            folder_name = replace_special_character(extra)
                        else :
                            folder_name = folder_name + "_" + replace_special_character(extra)                
                    anArchiver = archiver.Archiver(remove=self.remove)
                    anArchiver.addSource(source.Directory(root,recursive=False))
                    docsStorage= storage.GoogleDocs(self.login, self.password, folder=folder_name)
                    mediaStorage = storage.Picassa(self.login, self.password, album=folder_name)
                    raidStorage = storage.AggregatorStorage()
                    raidStorage.addStorage(mediaStorage)
                    raidStorage.addStorage(docsStorage)
                    anArchiver.addStorage(raidStorage)    
                    if self.verbose :
                        pl = progressListener
                        if pl is None :
                            pl = archiver.verboseProgressListener()
                        anArchiver.save(progress_listener=pl)
                    else:
                        anArchiver.save()
 
        else :
            anArchiver = archiver.Archiver(remove=self.remove) 
            for dir in self.dirs:
                anArchiver.addSource(source.Directory(dir))    
            docsStorage= storage.GoogleDocs(self.login, self.password, folder=self.folder)
            mediaStorage = storage.Picassa(self.login, self.password, album=self.folder)
            raidStorage = storage.AggregatorStorage()
            raidStorage.addStorage(mediaStorage)
            raidStorage.addStorage(docsStorage)
            anArchiver.addStorage(raidStorage)    
            if self.verbose :
                pl = progressListener
                if pl is None :
                    pl = archiver.verboseProgressListener()
                anArchiver.save(progress_listener=pl)
            else:
                anArchiver.save()
      