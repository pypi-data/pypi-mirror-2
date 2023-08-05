# -*- encoding: UTF-8 -*-
'''
Created on 5 avr. 2010

@author: thierry
'''

import sys, os

import caritang.core.archiver
import caritang.core.source
import caritang.core.storage

from caritang.common import version 

from optparse import OptionParser


version.getInstance().submitRevision("$Revision: 31 $")


def replace_special_character(a_string):
    return a_string.replace("/","_").replace(".","") # to be modified if needed

def backupDir(login, password, folder, remove=False, flatten=False, *dirs ):
    '''
    Backup one or more given directories
    '''
   
    
    if flatten :
        for dir in dirs: 
            # generate as many remote directory as subfolder in local directory
            for root, dir_list, files in os.walk(dir) :
                folder_name = folder
                extra = root.partition(dir)[2] # part after dir
                if len(extra) > 0 :
                    if folder_name is None:
                        folder_name = replace_special_character(extra)
                    else :
                        folder_name = folder_name + "_" + replace_special_character(extra)
                anArchiver = caritang.core.archiver.Archiver()
                anArchiver.addSource(caritang.core.source.Directory(root,recursive=False))
                docsStorage= caritang.core.storage.GoogleDocs(login, password, folder=folder_name)
                mediaStorage = caritang.core.storage.Picassa(login, password, album=folder_name)
                raidStorage = caritang.core.storage.AggregatorStorage()
                raidStorage.addStorage(mediaStorage)
                raidStorage.addStorage(docsStorage)
                anArchiver.addStorage(raidStorage)    
                anArchiver.save()
 
    else :
        anArchiver = caritang.core.archiver.Archiver() 
        for dir in dirs:
            anArchiver.addSource(caritang.core.source.Directory(dir))    
        docsStorage= caritang.core.storage.GoogleDocs(login, password, folder=folder)
        mediaStorage = caritang.core.storage.Picassa(login, password, album=folder)
        raidStorage = caritang.core.storage.AggregatorStorage()
        raidStorage.addStorage(mediaStorage)
        raidStorage.addStorage(docsStorage)
        anArchiver.addStorage(raidStorage)    
        anArchiver.save()
    

    
def run():
   versionManager = version.getInstance()
   usage = "%prog -l <login> -p <pasword>  [-d <destination>] [-r] [-f] directory ..."
   str_version = "%prog " + versionManager.getVersion() + "(" + versionManager.getRevision() + ")"
   parser = OptionParser(usage=usage, version=str_version)

   parser.add_option("-l","--login",action="store", dest="login", help="the login of the user without the @gmail")
   parser.add_option("-p","--password",action="store", dest="password", help="the password for the given login")
   parser.add_option("-d","--destination",action="store", dest="folder", help="the rmote folder or album name")
   parser.add_option("-r","--remove",action="store_true", dest="remove",  default=False, help="remove local file when uploaded")
   parser.add_option("-f","--flatten",action="store_true", dest="flatten", default=False, help="subfolder are flattened to folder with name prefixed by given -d option value if any")
   
   (options, args) = parser.parse_args()
   
   backupDir(options.login, options.password, options.folder, options.remove, options.flatten, *args)



if __name__ == '__main__':
    argline = sys.argv
    run()
