# -*- encoding: UTF-8 -*-
'''
Created on Apr 18, 2010

@author: maemo
'''

import gtk
import hildon
import gobject
import logging
import sys, traceback
import os.path
import webbrowser
import logging
import threading
import time
from Queue import *

import gdata.projecthosting.client
import gdata.projecthosting.data
import gdata.gauth
import gdata.client
import gdata.data
import atom.http_core
import atom.core

import caritang.core.archiver

from caritang.common import version

version.getInstance().submitRevision("$Revision: 155 $")

gtk.gdk.threads_init()


class CaritangGui(object):
    '''
    This is the GUI of Caritang
    '''


    def __init__(self, mocked=False):
        '''
        Create a new application GUI
        '''
        self.program = hildon.Program.get_instance()
        if mocked :
           self.zcore = None # TODO
        else:
           self.zcore = None # TODO
       
        self._last_opened_folder = "/home/user/MyDocs"
        self.__exception_fifo__ = Queue(0)
        self.exception_signal_handler_id = gobject.timeout_add(1000, self.receive_exception_signal)

        self.init_main_view()   
 


    def _default_exception_handler(self):
        '''
        Do appropriate action when the core throw a Exception.
        Currently simply display a banner message.
        '''
        type, value,tb = sys.exc_info() 
        self.__default_exception_handler(type, value, tb)
        
    def __default_exception_handler(self, type, value, tb):
        logging.exception("!!! UNHANDLED EXCEPTION !!!")      
        self.show_banner_information("An exception occured, please report the bug")     
        window = BugReportView(type, value, tb, self.submit_issue)
        self.init_menu(window)
        self.program.add_window(window)
        window.show_all()
    

    def send_exception_signal(self):
        '''
        Thread other than Gtk main, must call this method to post an exception
        '''
        self.__exception_fifo__.put(sys.exc_info())
        
    def receive_exception_signal(self):
        '''
        This method take an exception from the FIFO list of exception and
        display the corresponding GUI
        '''
        try:
            type, value, tb = self.__exception_fifo__.get_nowait()
            self.__default_exception_handler(type, value, tb)
        except Empty:
            pass
        return True
            

    def _call_handled_method(self, method, *arg):
        try:
            method(*arg)
        except :
            # this is an unkown exception
            self._default_exception_handler()


    def _refresh_from_menu(self):
        '''
        the user has request to refresh the view
        '''
        view = hildon.WindowStack.get_default().peek()        
        # disable the cache mechanisme of caritang
        self.zcore.setForceRefresh(True)
        try:
            view.refresh()
        finally:
            self.zcore.setForceRefresh(False)


    def _restore_default_settings(self):
        self.zcore.applyDefaultSettings()
        self.show_banner_information("default settings restored")
        # remove  the view
        hildon.WindowStack.get_default().pop_1()


    def _save_settings(self, settings):
        self.zcore.applyAndSaveSettings(settings)
        self.show_banner_information("setting saved")
        # remove  the view
        hildon.WindowStack.get_default().pop_1()

    def init_main_view(self):
        '''
        create a new window for the main view of the application
        '''
       
        # display a spashscreen
        window = SplashScreenView()       
        self.init_menu(window)
        self.program.add_window(window)       
        window.connect("destroy", self.quit_application, None)
        # This call show the window and also add the window to the stack
        window.show_all()

        # TODO do some stuff here                        

    def quit_application(self, widget, data):
        gobject.source_remove(self.exception_signal_handler_id)
        gtk.main_quit()
    
    def init_menu(self, window):
        '''
        create menu for all windows that will be used
        in this program
        '''
        menu = hildon.AppMenu()
                                                   
        newMenuBtn = hildon.GtkButton(gtk.HILDON_SIZE_AUTO);
        newMenuBtn.set_label("New");
        newMenuBtn.connect("clicked", self.backup_one_directory_from_menu, None)
        menu.append(newMenuBtn)                                                   
                                                   
        defaultMenuBtn = hildon.GtkButton(gtk.HILDON_SIZE_AUTO);
        defaultMenuBtn.set_label("Default");
        defaultMenuBtn.connect("clicked", self.backup_default_directory_from_menu, None)
        menu.append(defaultMenuBtn)                                                   

        
        paramMenuBtn = hildon.GtkButton(gtk.HILDON_SIZE_AUTO);
        paramMenuBtn.set_label("Settings");
        paramMenuBtn.connect("clicked", self.show_settings_from_menu, None)
        menu.append(paramMenuBtn)
    
        aboutMenuBtn = hildon.GtkButton(gtk.HILDON_SIZE_AUTO);
        aboutMenuBtn.set_label("About");
        aboutMenuBtn.connect("clicked", self.show_about_dialog, None)
        menu.append(aboutMenuBtn)   
        
        menu.show_all()
        window.set_app_menu(menu)  
        
    
    def backup_default_directory_from_menu(self, widget, data):
        '''
        Backup default directory e.g. /home/user/MyDocs/DCIM and /home/user/MyDocs/.documents
        '''        
        self.backup_default_directory()
        
    def backup_default_directory(self):
        parent = hildon.WindowStack.get_default().peek()
        dialog = hildon.LoginDialog(parent)
        dialog.set_message("Gmail account required")            
        response = dialog.run()
        self._login = dialog.get_username()
        self._password = dialog.get_password()
        dialog.destroy()
        if response == gtk.RESPONSE_OK:
            ccore = caritang.core.caritang.Caritang.getN900DefaultInstance(self._login, self._password)          
            window = ProgressView()
            self.program.add_window(window)                       
            backup_thread = AsyncBackup(ccore, window.getProgressListener(), self)
            window.connect("destroy", self.destroy_progress_window,  backup_thread)
            window.show_all()
            backup_thread.start()
            self.show_banner_information("backup started")                 
        else:
            self.show_banner_information("backup cancelled")
        
        
    def destroy_progress_window(self,  widget,  backup_thread):
         backup_thread.send_stop_signal()     
    
    def backup_one_directory_from_menu(self, widget, data):
        parent = hildon.WindowStack.get_default().peek()
        fc = gobject.new(hildon.FileChooserDialog, action=gtk.FILE_CHOOSER_ACTION_OPEN)
        fc.set_property('show-files',True)    
        fc.set_current_folder(self._last_opened_folder)
        if fc.run()==gtk.RESPONSE_OK: 
            filepath = fc.get_filename()
            fc.destroy()
            self._last_opened_folder = os.path.dirname(filepath)  
            # TODO open a windows to select parameter : destination and flatten/resume option           
        else:
            fc.destroy()
        

    def refresh_from_menu(self, widget, data):
        self._call_handled_method(self._refresh_from_menu)

    def show_note_information(self, mess):
       parent = hildon.WindowStack.get_default().peek()
       note = hildon.hildon_note_new_information(parent,mess)                 
   
       response = gtk.Dialog.run(note)

    def show_banner_information(self, mess):
       parent = hildon.WindowStack.get_default().peek()
       banner= hildon.hildon_banner_show_information(parent,"", mess)
       banner.set_timeout(2000)     
    
    def show_settings_from_menu(self, widget, data):
        '''
        Show settings dialog
        '''
        window = SettingsView(self.save_settings, self.restore_default_settings,  self.zcore)
        
        self.init_menu(window)
        self.program.add_window(window)
        window.show_all()

    def save_settings(self, settings):
        self._call_handled_method(self._save_settings,settings)

    def restore_default_settings(self):
        self._call_handled_method(self._restore_default_settings)


    def show_about_dialog(self, widget, data):
       '''
       Show an information dialog about the program
       '''
       window = AboutView()
        
       self.program.add_window(window)
       window.show_all()
       
    def submit_issue(self, title, description):
        # check credential
        try:
            parent = hildon.WindowStack.get_default().peek()
            dialog = hildon.LoginDialog(parent)
            dialog.set_message("Gmail account required")            
            response = dialog.run()
            username = dialog.get_username()
            password = dialog.get_password()
            dialog.destroy()
            if response == gtk.RESPONSE_OK:
                try:
                    issues_client = gdata.projecthosting.client.ProjectHostingClient()
                    issues_client.client_login(username, password,"caritang", "code")
                    versionInstance = version.getInstance()
                    versionStr = versionInstance.getVersion()
                    revisionStr = versionInstance.getRevision()
                    labels = ['Type-Defect', 'Priority-High', 'Version-' + versionStr, 'Revision-' + revisionStr]
                    issues_client.add_issue("caritang", title, description, "tbressure", labels=labels)
                except:                    
                    self.show_banner_information("failed to send issue")
                    logging.exception("Failed to report the previous issue due to")
                else:
                    self.show_banner_information("issue sent")
            else:
                self.show_banner_information("bug report cancelled")
        finally:
            hildon.WindowStack.get_default().pop_1()

    
    def run(self):
        # the splash screen  is displayed,now show the home screen in a fancy tansition               
        gtk.main()


class AsyncBackup(threading.Thread):
        def __init__(self, ccore, progress_listener, caritang_gui):
            threading.Thread.__init__(self,name="Caritang-AsyncBackup")                    
            self.setDaemon(True)   
            self.ccore = ccore
            self.progress_listener = progress_listener
            self.caritang_gui = caritang_gui
        
        def run(self):            
            logging.info("async backup thread running....")                           
            self.cancellableAction()            
            logging.info("async backup thread finished")

        def cancellableAction(self):
            try:
                self.ccore.save(self.progress_listener)
            except StopSignalException, sse:
                logging.info("async backup aborted")
            except:
                logging.error("uncaught exception in async backup")
                self.caritang_gui.send_exception_signal()
            else:
                logging.info("async backup terminated")
            
        def send_stop_signal(self):
            self.progress_listener.send_stop_signal()
        
class StopSignalException(Exception):
    pass

class CaritangStackableWindow(hildon.StackableWindow):
    '''
    general design of any GUI of this app
    '''
    
    centerview = None;
    bottomButtons = None;
    
    def __init__(self, title="Caritang"):
        hildon.StackableWindow.__init__(self)
        self.set_title(title)
   
        container = gtk.VBox();                
                  
        self.centerview = gtk.VBox() 
        
        self.init_center_view(self.centerview)
        
        pannable_area = hildon.PannableArea()
        pannable_area.set_property('mov_mode',hildon.MOVEMENT_MODE_BOTH)
        pannable_area.add_with_viewport(self.centerview)
        
        self.bottomButtons = gtk.HBox(homogeneous=True)
        
        self.init_bottom_button(self.bottomButtons)
        

        bottomAlign = gtk.Alignment(0.5,0,0,0)
        bottomAlign.add(self.bottomButtons)
        
        container.pack_start(pannable_area)
        container.pack_start(bottomAlign, expand=False)
        
        self.add(container)

    def init_center_view(self, centerview):
        '''
        This hook should be implemented by subclass to
        add widget in the centerview which is both instance
        and attribute variable for convenience
        '''
        pass;
    
    def init_bottom_button(self, bottomButtons):
        '''
        This hook should be implemented by subclass to
        add button in the bottom button which is both instance
        and attribute variable for convenience
        '''
        pass;

    def add_button(self, button):
        '''
        goodies to add a button to this view
        '''
        self.bottomButtons.pack_start(button,True,True,0)
    
    def create_button(self, name, value=None):
        '''
        goodies to create a button for this view
        ''' 
        return hildon.Button(gtk.HILDON_SIZE_THUMB_HEIGHT, hildon.BUTTON_ARRANGEMENT_HORIZONTAL, name, value)

    def justifyLeft(self, widget):
          leftAlign = gtk.Alignment(0,0.5,0,0)
          leftAlign.add(widget)
          return leftAlign

class AboutView(CaritangStackableWindow):
    '''
    This view show a fancy about dialog
    '''

    def init_center_view(self, centerview):
        
        pixbuf = gtk.gdk.pixbuf_new_from_file("caritang-logo.png")
        image = gtk.Image()
        image.set_from_pixbuf(pixbuf)
        centerview.add(image)
        
        centerview.add(gtk.Label("Caritang - " + version.getInstance().getVersion()))
        centerview.add(gtk.Label("Backup application to Google for N900"))
        centerview.add(gtk.Label("by Thierry Bressure - http://blog.caritang.bressure.net"))


    def init_bottom_button(self, bottomButtons):
        blogButton = self.create_button("Blog")
        blogButton.connect("clicked", self.on_blog_clicked_event, None)
        self.add_button(blogButton)
        
        siteButton = self.create_button("Site")
        siteButton.connect("clicked", self.on_site_clicked_event, None)
        self.add_button(siteButton)
        
        groupsiteButton = self.create_button("Groups")
        groupsiteButton.connect("clicked", self.on_group_clicked_event, None)
        self.add_button(groupsiteButton)

    def on_blog_clicked_event(self, widget, data):
         webbrowser.open_new_tab("http://blog.caritang.bressure.net");
    
    def on_site_clicked_event(self, widget, data):
         webbrowser.open_new_tab("http://caritang.bressure.net");
         
    def on_group_clicked_event(self, widget, data):
         webbrowser.open_new_tab("http://group.caritang.bressure.net");
             
    

class SplashScreenView(CaritangStackableWindow):
    '''
    This is the first view of the application e.g. the main view.  
    '''

    def init_center_view(self, centerview):
        pixbuf = gtk.gdk.pixbuf_new_from_file("caritang-logo.png")
        for i in range(1,4):
            hbox = gtk.HBox()
            for j in range(1,5):                
                image = gtk.Image()
                image.set_from_pixbuf(pixbuf)
                hbox.add(image)
            centerview.add(hbox)


class ProgressView(CaritangStackableWindow, caritang.core.archiver.ProgressListener):
    '''
    This view show backup progress
    '''
    
    def __init__(self):
        
        self.num_processed_item = 0
        self.num_skipped_item = 0
        self.num_aborted_item = 0
        self.num_uploaded_item = 0
        self.num_removed_item = 0     
        
        self.progressListener = ProgressListener(self)
        
        CaritangStackableWindow.__init__(self, title="Backup")        



    def getProgressListener(self):
        return self.progressListener

 
    def init_center_view(self, centerview):
        
        tableView = gtk.Table(6, 2, False)
        
        self.num_processed_item_label = gtk.Label("0")             
        caption_processed = self.justifyLeft(gtk.Label("processed item"))         
        tableView.attach(caption_processed,0,1,0,1)
        tableView.attach(self.justifyLeft(self.num_processed_item_label),1,2,0,1,xpadding=10)
        
        
        self.num_skipped_item_label = gtk.Label("0")                            
        caption_skipped = self.justifyLeft(gtk.Label("skipped item"))        
        tableView.attach(caption_skipped,0,1,1,2)
        tableView.attach(self.justifyLeft(self.num_skipped_item_label),1,2,1,2,xpadding=10)        

        self.num_aborted_item_label = gtk.Label("0")                                 
        caption_aborted = self.justifyLeft(gtk.Label("aborted item"))        
        tableView.attach(caption_aborted,0,1,2,3)
        tableView.attach(self.justifyLeft(self.num_aborted_item_label),1,2,2,3,xpadding=10)                           
        
        self.num_uploaded_item_label = gtk.Label("0")                  
        caption_uploaded = self.justifyLeft(gtk.Label("uploaded item"))          
        tableView.attach(caption_uploaded,0,1,3,4)
        tableView.attach(self.justifyLeft(self.num_uploaded_item_label),1,2,3,4,xpadding=10)             
 
        self.num_removed_item_label = gtk.Label("0")                        
        caption_removed = self.justifyLeft(gtk.Label("removed item"))        
        tableView.attach(caption_removed,0,1,4,5)
        tableView.attach(self.justifyLeft(self.num_removed_item_label),1,2,4,5,xpadding=10) 
        
        self.status_label = gtk.Label("idle")                        
        caption_status = self.justifyLeft(gtk.Label("status"))        
        tableView.attach(caption_status,0,1,5,6)
        tableView.attach(self.justifyLeft(self.status_label),1,2,5,6,xpadding=10) 
        
        centerview.add(tableView)    
                 
    
     


    def init_bottom_button(self, bottomButtons):
        return CaritangStackableWindow.init_bottom_button(self, bottomButtons)


    def _add_new_processed_item(self, doc_item):
        self.num_processed_item = self.num_processed_item + 1
        self.num_processed_item_label.set_text(str(self.num_processed_item))              
        

    def _add_new_skipped_item(self, doc_item):
        self.num_skipped_item = self.num_skipped_item + 1
        self.num_skipped_item_label.set_text(str(self.num_skipped_item))        
       
        
    def _add_new_aborted_item(self, doc_item):
        self.num_aborted_item = self.num_aborted_item + 1
        self.num_aborted_item_label.set_text(str(self.num_aborted_item))
        
        
    def _add_new_uploaded_item(self, doc_item):
        self.num_uploaded_item = self.num_uploaded_item + 1
        self.num_uploaded_item_label.set_text(str(self.num_uploaded_item))
        

    def _add_new_removed_item(self, doc_item):
        self.num_removed_item = self.num_removed_item + 1
        self.num_removed_item_label.set_text(str(self.num_removed_item))
        
        
    def _set_status(self, status):
        self.status_label.set_text(status)
        
    
    def _clear_status(self):
        self.status_label.set_text("idle")
        


class ProgressListener(caritang.core.archiver.ProgressListener):
    '''
    Progress listener interface
    '''
    
    def __init__(self, view):
        self.stop_signal_received = False
        self.view = view

    def send_stop_signal(self):
        self.stop_signal_received = True
    
    def _handle_stop_signal(self):
        if self.stop_signal_received:
            raise StopSignalException("Stop signal received")
    
    
    def startSaveDocItem(self, doc_item):  
        self._handle_stop_signal()  
        gtk.gdk.threads_enter()
        message = "processing " + doc_item.getFile()    
        self.view._set_status(message)
        self.view._add_new_processed_item(doc_item)
        gtk.gdk.threads_leave()
#        time.sleep(10)

    def endSaveDocItem(self, docItem, storage, status):   
        self._handle_stop_signal()       
        gtk.gdk.threads_enter()
        self.view._clear_status()
        if status == caritang.core.archiver.SAVED_SUCCESS:
            self.view._add_new_uploaded_item(docItem)
        elif status == caritang.core.archiver.SAVED_FAILURE:
            self.view._add_new_aborted_item(docItem)
        elif status == caritang.core.archiver.SAVED_ALREADY:
            self.view._add_new_skipped_item(docItem)
        else:
            logging.error("progress listener : unhandled status " + status)
        pass
        gtk.gdk.threads_leave()

    def startRemoveDocItem(self, docItem):
        self._handle_stop_signal()  
        self.view._set_status("removing "  + docItem.getFile())
        pass

    def endRemoveDocItem(self, docItem, status):
        self._handle_stop_signal()  
        gtk.gdk.threads_enter()
        self.view._clear_status()
        if status == caritang.core.archiver.REMOVED_SUCCESS:
            self.view._add_new_removed_item(docItem)
        pass
        gtk.gdk.threads_leave()


    def handleCaptcha(self, url, storage):
        self._handle_stop_signal()  
        return caritang.core.archiver.ProgressListener.handleCaptcha(self, url, storage)
        pass


    def connectToStorage(self, storgae, status):
        self._handle_stop_signal()  
        pass


       

class BugReportView(CaritangStackableWindow):
    '''
    This view show the bug and give the user the opportunity to report it
    '''
    type = None
    value = None
    traceback = None
    
    submit_issue_callback = None
    
    _body = None
    _subject = None
    
    def __init__(self, type, value, traceback, submit_issue_callback):
        self.type = type
        self.value = value
        self.traceback = traceback
        self.submit_issue_callback = submit_issue_callback
        CaritangStackableWindow.__init__(self, title="Bug reporting") 

    def init_center_view(self, centerview):
       
        subjectLbl = gtk.Label("Subject")
        centerview.pack_start(self.justifyLeft(subjectLbl), False)
        self._subject = hildon.Entry(gtk.HILDON_SIZE_FULLSCREEN_WIDTH)
        self._subject.set_placeholder("enter a subject")
        self._subject.set_text(str(self.type) + " : " + str(self.value))
        centerview.pack_start(self._subject, False)
        contentLbl = gtk.Label("Content")
        centerview.pack_start(self.justifyLeft(contentLbl), False)
        self._body = hildon.TextView()
        self._body.set_placeholder("enter the message here")
        self._body.set_wrap_mode(gtk.WRAP_WORD)
        stacktrace = traceback.format_exception(self.type, self.value, self.traceback)
        buf = self._body.get_buffer()
        for line in stacktrace:
            end = buf.get_end_iter()
            buf.insert(end, line, len(line))
        centerview.add(self._body)
        return CaritangStackableWindow.init_center_view(self, centerview)


    def init_bottom_button(self, bottomButtons):
        post = self.create_button("Post issue", None)
        post.connect("clicked", self.on_post_button_clicked, self)
        self.add_button(post)                     
        return CaritangStackableWindow.init_bottom_button(self, bottomButtons)

    def on_post_button_clicked(self, widget, view):
        buffer = view._body.get_buffer()
        body = buffer.get_text(buffer.get_start_iter(), buffer.get_end_iter())
        subject =  view._subject.get_text()
        self.submit_issue_callback(subject, body)

class SettingsView(CaritangStackableWindow):
    '''
    View to manage settings of the application.
    '''
    
    def __init__(self, save_callback, default_callback,  zcore):        
        self.zcore = zcore
        self.save_callback = save_callback
        self.default_callback = default_callback

        CaritangStackableWindow.__init__(self, "Settings")


    def init_center_view(self, centerview):
        pass        
        
 
    def init_bottom_button(self, bottomButtons):
        saveBtn = self.create_button("Save")
        saveBtn.connect("clicked", self.on_save_clicked, self)
        self.add_button(saveBtn)
        defaultBtn = self.create_button("Default")
        defaultBtn.connect("clicked", self.on_default_clicked, self)
        self.add_button(defaultBtn)
      
    def on_save_clicked(self, widget, data):
        pass

    def on_default_clicked(self, widget, data):
        pass



        