'''
Created on 5 avr. 2010

@author: thierry
'''

import os.path
import mimetypes
import gdata.docs
import gdata.docs.service

import gdata.photos.service
import gdata.media
import gdata.geo

from caritang.common import version 

version.getInstance().submitRevision("$Revision: 9 $")

NOT_YET_IMPLEMENTED = 'not yet implemented'

class DocStorage(object):
    '''
    Interface of DocStorage e.g. place where store document to.
    '''
    
    def store(self, doc):
        raise RuntimeError(NOT_YET_IMPLEMENTED)
    
    def canStore(self, doc):
        '''
        Test is this storage can store the document
        '''
        raise RuntimeError(NOT_YET_IMPLEMENTED)

class CaritangStorageException(Exception):
    pass
            
    
class AggregatorStorage(DocStorage):
    '''
    This storage aggregate several storage to provide a seemless storage
    that can handle all documents of each aggregated storage.
    '''
    
    def __init__(self):
        self.storages = []

    def store(self, doc):
        capables = filter(lambda(storage): storage.canStore(doc), self.storages)
        if len(capables) == 0:
            raise CaritangStorageException()
        storage = capables[0]
        storage.store(doc)

    def canStore(self, doc):
        for storage in self.storages:
            if storage.canStore(doc) :
                return True
        return False
    
    def addStorage(self, storage):
        self.storages.append(storage)
        
    
    
class Picassa(DocStorage):
    '''
    This is the Picassa implementation for a storage.
    '''
    def __init__(self, login, password, album=None):
        '''
        Create a Picassastorage. If provided folder parameter is the folder
        where data will be uploaded.
        Note : login must contains the @gmail.com part        
        '''
        self.login = login
        
        self.gd_client = gdata.photos.service.PhotosService()
        self.gd_client.email = login
        self.gd_client.password = password
        self.gd_client.source = 'bressure.net-caritang-v1'
        self.gd_client.ProgrammaticLogin()
        
        self.album = album
        self.ensure_destination_folder()

    def canStore(self, doc):
        type = mimetypes.guess_type(doc,strict=False)[0]    
        if type == "image/jpeg" \
           or type == "video/mp4" :
            return True
        return False
           

    
    
    def ensure_destination_folder(self):
        '''
        Check existence of destination folder and create it if needed
        '''
        if self.album is not None:
            albums = self.gd_client.GetUserFeed()            
            remoteAlbum = filter(lambda(entry): entry.title.text == self.album, albums.entry)
            if len(remoteAlbum) == 0 :
                self.album_entry = self.gd_client.InsertAlbum(title=self.album, summary='Album for N900 media')
            else :
                self.album_entry = remoteAlbum[0]    
    
    def store(self, doc):
        '''
        store the given doc to the storage
        '''      
        type = mimetypes.guess_type(doc,strict=False)[0]        
        photoName = os.path.basename(doc)
        if self.album is None:
            photo = self.gd_client.InsertPhotoSimple('/data/feed/api/user/default/albumid/default', photoName, 
                                               'Uploaded using the API', doc, content_type='image/jpeg')
        else :
            album_url = '/data/feed/api/user/%s/albumid/%s' % (self.login, self.album_entry.gphoto_id.text)
            photo = self.gd_client.InsertPhotoSimple(album_url, photoName, 
                            'Uploaded using the API', doc, content_type='image/jpeg')                   

        
               
            
        
    def __str__(self):
        return "Picassa for " + self.login

class GoogleDocs(DocStorage):
    '''
    This is the google docs implementation for a storage.
    '''


    def __init__(self, login, password, folder=None):
        '''
        Create a google doc storage. If provided folder parameter is the folder
        where data will be uploaded.
        Note : login must contains the @gmail.com part        
        '''
        self.login = login
        self.gd_client = gdata.docs.service.DocsService(source='bressure.net-caritang-v1')
        self.gd_client.ClientLogin(login, password)
        
        self.folder = folder
        self.ensure_destination_folder()

    def canStore(self, doc):
        return False # inhibate google doc 
    
    
    def ensure_destination_folder(self):
        '''
        Check existence of destination folder and create it if needed
        '''
        if self.folder is not None:
            q = gdata.docs.service.DocumentQuery(categories=['folder'], params={'showfolders': 'true'})
            feed = self.gd_client.Query(q.ToUri())
            remoteFolder = filter(lambda(entry): entry.title.text == self.folder, feed.entry)
            if len(remoteFolder) == 0 :
                self.folder_entry = self.gd_client.CreateFolder(self.folder)
            else :
                self.folder_entry = remoteFolder[0]    
   
    
    def store(self, doc):
        '''
        store the given doc to the storage
        '''      
        type = mimetypes.guess_type(doc,strict=False)[0]        
               
        ms = gdata.MediaSource(file_path=doc, content_type=type)
        if self.folder is None:
            entry = self.gd_client.Upload(ms, os.path.basename(doc))            
        else :
            entry = self.gd_client.Upload(ms, os.path.basename(doc), folder_or_uri=self.folder_entry)
        
               
            
        
    def __str__(self):
        return "google docs for " + self.login