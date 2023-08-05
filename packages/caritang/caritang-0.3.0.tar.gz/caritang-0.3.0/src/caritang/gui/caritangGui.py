# -*- encoding: UTF-8 -*-
'''
Created on Apr 18, 2010

@author: maemo
'''

import gtk
import hildon
import logging
import sys, traceback
import webbrowser


import gdata.projecthosting.client
import gdata.projecthosting.data
import gdata.gauth
import gdata.client
import gdata.data
import atom.http_core
import atom.core

from caritang.common import version

version.getInstance().submitRevision("$Revision: 155 $")

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
       
        self.init_main_view()   


    def _default_exception_handler(self):
        '''
        Do appropriate action when the core throw a Exception.
        Currently simply display a banner message.
        '''
        #TODO open a window with the stack trace and ask to send the bug report            
        logging.exception("!!! UNHANDLED EXCEPTION !!!")      
        self.show_banner_information("An exception occured, please report the bug")
        type, value,tb = sys.exc_info() 
        window = BugReportView(type, value, tb, self.submit_issue)
        self.init_menu(window)
        self.program.add_window(window)
        window.show_all()
                        
        

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
        window.connect("destroy", gtk.main_quit, None)
        # This call show the window and also add the window to the stack
        window.show_all()

        # TODO do some stuff here                        

    def init_menu(self, window):
        '''
        create menu for all windows that will be used
        in this program
        '''
        menu = hildon.AppMenu()
                                                   
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
          leftAlign = gtk.Alignment(0,0,0,0)
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
        centerview.add(gtk.Label("Caritang generated by template"))
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



        