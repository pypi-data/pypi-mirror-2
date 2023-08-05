'''
Created on 5 avr. 2010

@author: thierry
'''
import logging

import os.path
import mimetypes
import gdata.docs
import gdata.docs.service

import gdata.photos.service
import gdata.media
import gdata.geo

from caritang.common import version 

version.getInstance().submitRevision("$Revision: 73 $")

NOT_YET_IMPLEMENTED = 'not yet implemented'

class DocStorage(object):
    '''
    Interface of DocStorage e.g. place where store document to.
    '''
    
    def store(self, doc):
        '''
        Store the docItem
        '''
        raise RuntimeError(NOT_YET_IMPLEMENTED)
    
    def canStore(self, doc):
        '''
        Test is this storage can store the document.
        The document is e DocItem
        '''
        raise RuntimeError(NOT_YET_IMPLEMENTED)
    
    def getName(self):
        '''
        The name of the storage
        '''
        raise RuntimeError(NOT_YET_IMPLEMENTED)
    
    def connect(self, captcha=None, response=None):
        '''
        connect the storage to the google service.
        This method generally call programmaticLogin.
        The caller must handle CaritangCaptchaException
        '''
        raise RuntimeError(NOT_YET_IMPLEMENTED)
        
    def isConnected(self):
        '''
        Test is the storage is connected
        '''
        raise RuntimeError(NOT_YET_IMPLEMENTED)


class CaritangStorageException(Exception):
    pass


class CaritangCaptchaException(Exception):
    '''
    Login failure because google required a capcha
    '''            
    
    def __init__(self, token, url, doc_storage=None):
        self.captcha_token = token
        self.captcha_url = url
        self.doc_storage = doc_storage
        
    def get_token(self):
        return self.captcha_token
    
    def get_url(self):
        return self.captcha_url
    
    def get_storage(self):
        return self.doc_storage
    
class AggregatorStorage(DocStorage):
    '''
    This storage aggregate several storage to provide a seemless storage
    that can handle all documents of each aggregated storage.
    '''
    
    def __init__(self):
        self.storages = []

    def connect(self, captcha=None, response=None):
        for a_storage in self.storages:
           a_storage.connect(captcha, response)                 


    def isConnected(self):
        return not False in map(lambda(storage): storage.isConnected(), self.storages)


    def getName(self):
        return "aggregator"


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
    
    mimetypes.add_type("video/mp4", ".mp4")
    mimetypes.add_type("image/png", ".png")
    mimetypes.add_type("image/gif", ".gif")
    gdata.photos.service.SUPPORTED_UPLOAD_TYPES = gdata.photos.service.SUPPORTED_UPLOAD_TYPES + ("mp4",)
    
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
        
        self.__is_connected = False                
        self.album = album


    def getName(self):
        return "Picasa"

        

    def isConnected(self):
        return self.__is_connected

    def connect(self, captcha=None, response=None):
        try : 
            self.gd_client.ProgrammaticLogin(captcha, response)
            self.__is_connected = True
            self.ensure_destination_folder()
        except gdata.service.CaptchaRequired:
            raise CaritangCaptchaException(self.gd_client._GetCaptchaToken(), self.gd_client._GetCaptchaURL(), self)        

    def canStore(self, doc):
        type = mimetypes.guess_type(doc.getName(),strict=False)[0]    
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
                self.album_entry = self.gd_client.InsertAlbum(title=self.album, summary='Album created by Caritang', access='protected')                
            else :
                self.album_entry = remoteAlbum[0]    
    
    def store(self, docItem):
        '''
        store the given doc to the storage
        '''      
        doc = docItem.getFile()
        type = mimetypes.guess_type(doc,strict=False)[0]        
        photoName = os.path.basename(doc)
        try:
            if self.album is None:
                photo = self.gd_client.InsertPhotoSimple('/data/feed/api/user/default/albumid/default', photoName, 
                                                         'Uploaded with Caritang', doc, content_type=type)
            else :
                album_url = '/data/feed/api/user/%s/albumid/%s' % (self.login, self.album_entry.gphoto_id.text)            
                photo = self.gd_client.InsertPhotoSimple(album_url, photoName, 
                                                         'Uploaded with Caritang', doc, content_type=type)                   
        except gdata.photos.service.GooglePhotosException:
            logging.exception("Failed to save picture")
            raise CaritangStorageException() #TODO be more precise
        except IOError:
            logging.exception("Failed to save picture")
            raise CaritangStorageException() #TODO be more precise
            
        
    def __str__(self):        
        if self.album is None :        
            return "Picassa for " + self.login
        else:
            return "Picassa for " + self.login + " in " + self.album

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
        self.password = password
        self.gd_client = gdata.docs.service.DocsService(source='bressure.net-caritang-v1')        
        self.folder = folder        
        
        self.__is_connected = False

    def getName(self):
        return "Google docs"
    
    def isConnected(self):
        return self.__is_connected


    def connect(self, captcha=None, response=None):
        try : 
            self.gd_client.ClientLogin(self.login, self.password, captcha_token=captcha, captcha_response=response)
            self.__is_connected = True            
            self.ensure_destination_folder()
        except gdata.service.CaptchaRequired:
            raise CaritangCaptchaException(self.gd_client._GetCaptchaToken(), self.gd_client._GetCaptchaURL(), self)        


    
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
   
    
    def store(self, docItem):
        '''
        store the given doc to the storage
        '''      
        doc = docItem.getFile()
        type = mimetypes.guess_type(doc,strict=False)[0]        
               
        ms = gdata.MediaSource(file_path=doc, content_type=type)
        if self.folder is None:
            entry = self.gd_client.Upload(ms, os.path.basename(doc))            
        else :
            entry = self.gd_client.Upload(ms, os.path.basename(doc), folder_or_uri=self.folder_entry)
        
               
            
        
    def __str__(self):
        if self.folder is None : 
            return "google docs for " + self.login
        else : 
            return "google docs for " + self.login + " in" + self.folder