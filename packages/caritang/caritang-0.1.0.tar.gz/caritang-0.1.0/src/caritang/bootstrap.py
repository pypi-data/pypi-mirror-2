# -*- encoding: UTF-8 -*-
'''
Created on 5 avr. 2010

@author: thierry
'''

import sys

import caritang.core.archiver
import caritang.core.source
import caritang.core.storage

from caritang.common import version 

version.getInstance().submitRevision("$Revision: 12 $")

def backupDCIM(login, password, folder="N900"):
    '''
    Launch the backup of internal DCIM directory of the device and if availbale
    the external mmc card    
    '''
    internal_dcim = "/home/user/MyDocs/DCIM/"
    external_dcim = "/media/mmc1/DCIM/"
    anArchiver = caritang.core.archiver.Archiver()
    anArchiver.addSource(caritang.core.source.Directory(internal_dcim))
    anArchiver.addSource(caritang.core.source.Directory(external_dcim))
    docsStorage= caritang.core.storage.GoogleDocs(login, password, folder=folder)
    mediaStorage = caritang.core.storage.Picassa(login, password, album="N900")
    raidStorage = caritang.core.storage.AggregatorStorage()
    raidStorage.addStorage(mediaStorage)
    raidStorage.addStorage(docsStorage)
    anArchiver.addStorage(raidStorage)    
    anArchiver.save()
    
def run(argline):
    if len(argline) > 2 :          
        backupDCIM(argline[1], argline[2])
    else :
        print "usage : python bootstrap.py <login> <password>"
        print "ex : python bootstrap.py toto cghdygak"


if __name__ == '__main__':
    argline = sys.argv
    run(argline)
