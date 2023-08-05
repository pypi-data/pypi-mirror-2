# -*- encoding: UTF-8 -*-
'''
Created on 28 févr. 2010

@author: thierry
'''

import gtk
import hildon
from zourite.core import zourite, plugin # TODO i would like to remove this
import logging
import sys, traceback
import threading
import webbrowser
import mock

import dbus

import gdata.projecthosting.client
import gdata.projecthosting.data
import gdata.gauth
import gdata.client
import gdata.data
import atom.http_core
import atom.core

from zourite.common import version


version.getInstance().submitRevision("$Revision: 155 $")


class ZouriteGui():
   
    program = None 
    zcore = None
    
    def __init__(self, mocked=False):
   
       #zcore = zourite.Zourite()
       self.program = hildon.Program.get_instance()
       if mocked :
           self.zcore = mock.Zourite()
       else:
           self.zcore = zourite.Zourite()
       
       self.init_main_view()   

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


    def _refresh_from_menu(self):
        '''
    the user has request to refresh the view
    '''
        view = hildon.WindowStack.get_default().peek()        
        # disable the cache mechanisme of zourite
        self.zcore.setForceRefresh(True)
        try:
            view.refresh()
        finally:
            self.zcore.setForceRefresh(False)


    def _show_contact_list(self):
        
        window = ContactListView(self.select_contact, self.place_call, self.place_email, self.zcore)
        self.init_menu(window)
        self.program.add_window(window)
        window.show_all()

    def _show_network_update_connection_detail(self, netUpdateConn):
       
        myconn, newconn = self.zcore.getShortProfilesForNetUpdateConnection(netUpdateConn)
        window = NetworkUpdateConnectionView(myconn, newconn, self.show_detail_profil, self.show_invite_profile, self.zcore)
        self.init_menu(window)
        self.program.add_window(window)
        window.show_all()
        
    def _show_network_update_self_connection_detail(self, netUpdateConn):
       
        newconn = self.zcore.getShortProfileForNetUpdateSelfConnection(netUpdateConn)
        window = NetworkUpdateSelfConnectionView( newconn, self.show_detail_profil,self.zcore)
        self.init_menu(window)
        self.program.add_window(window)
        window.show_all()
        
        

    def _send_request_invite_profile(self, profile, subject, body):
        
            self.zcore.sendConnectionRequestToProfile(profile, subject, body)
            self.show_banner_information("invitation sent")
            # remove  the view
            hildon.WindowStack.get_default().pop_1()
       


    def _send_message_to_profile(self, profile, subject, body):
        
            self.zcore.sendMessageToProfile(profile, subject, body)
            self.show_banner_information("message sent to the contact")
            # remove  the view
            hildon.WindowStack.get_default().pop_1()
     


    def _show_detail_profil(self, shortProfile):
    
        fullProfile = self.zcore.getFullProfileForShortProfile(shortProfile)
        self.show_full_profile(fullProfile)
   


    def _send_message_to_network(self, message):
       
        self.zcore.sendMessageToNetwork(message)
        self.show_banner_information("message sent to the network")
        # remove  the view
        hildon.WindowStack.get_default().pop_1()
        
    
    def _clear_status(self):
       
        self.zcore.clearMyStatus()
        self.show_banner_information("status cleared")
        # remove  the view
        hildon.WindowStack.get_default().pop_1()
       


    def _modify_status(self, status):
      
        self.zcore.setMyStatus(status)
        self.show_banner_information("status updated")
        # remove  the view
        hildon.WindowStack.get_default().pop_1()       
 
    def _update_network_news(self, view):
        netUpdate = self.zcore.getNetworkUpdate()
        view.update_network_news(netUpdate, self.zcore)   
          
    def _select_contact(self, person):
        fullProfile = self.zcore.getFullProfileForShortPerson(person)
        self.show_full_profile(fullProfile)     
    
    def _show_update_status(self):
        setStatus = self.zcore.getAllMyStatus()
        window = UpdateStatusView(setStatus, self.modify_status, self.clear_status)
        self.init_menu(window)
        self.program.add_window(window)
        window.show_all()



    def _unavailable_handler(self):
        '''
        Do appropriate action when the core throw an UnvailableException.
        Currently simply display a banner message 
        '''
        return self.show_banner_information("The service is unavailable")

    def _configuration_required_handler(self):
        '''
        Do appropriate action when the core throw a ConfigurationRequieredException.
        Currently simply display a banner message
        '''
        return self.show_banner_information("The service need to be configured")
    
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
        except plugin.UnvailableException:
            self._unavailable_handler()
        except plugin.ConfigurationRequiredExeption:
            self._configuration_required_handler()
        except :
            # this is an unkown exception
            self._default_exception_handler()


    def _reset_cache(self):
        self.zcore.resetCacheData()
        self.show_banner_information("cache cleared")
    
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
                    issues_client.client_login(username, password,"zourite", "code")
                    versionInstance = version.getInstance()
                    versionStr = versionInstance.getVersion()
                    revisionStr = versionInstance.getRevision()
                    labels = ['Type-Defect', 'Priority-High', 'Version-' + versionStr, 'Revision-' + revisionStr]
                    issues_client.add_issue("zourite", title, description, "tbressure", labels=labels)
                except:                    
                    self.show_banner_information("failed to send issue")
                    logging.exception("Failed to report the previous issue due to")
                else:
                    self.show_banner_information("issue sent")
            else:
                self.show_banner_information("bug report cancelled")
        finally:
            hildon.WindowStack.get_default().pop_1()

    def show_full_profile(self, fullProfile):
        window = FullProfileView(fullProfile, self.show_invite_profile, self.show_message_profile, self.zcore)
        self.init_menu(window)
        self.program.add_window(window)
        window.show_all()


 
    def init_menu(self, window):
        '''
        create menu for all windows that will be used
        in this program
        '''
        menu = hildon.AppMenu()
           
        
        refreshMenuBtn = hildon.GtkButton(gtk.HILDON_SIZE_AUTO);
        refreshMenuBtn.set_label("Refresh");
        refreshMenuBtn.connect("clicked", self.refresh_from_menu, None)
        menu.append(refreshMenuBtn)
        
        contactMenuBtn = hildon.GtkButton(gtk.HILDON_SIZE_AUTO);
        contactMenuBtn.set_label("Contact");
        contactMenuBtn.connect("clicked", self.show_contact_list, None)
        menu.append(contactMenuBtn)   
        
        newsMenuBtn = hildon.GtkButton(gtk.HILDON_SIZE_AUTO);
        newsMenuBtn.set_label("News");
        newsMenuBtn.connect("clicked", self.show_network_news_from_menu, None)
        menu.append(newsMenuBtn)            
                
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
           
           
    def show_contact_list(self, widget, data):
        '''
        show the contact list window
        '''
        self._call_handled_method(self._show_contact_list)

    def select_contact(self, person):
        '''
        Bring up a gui showing a contact
        '''
        self._call_handled_method(self._select_contact, person)
        
    
    def show_settings_from_menu(self, widget, data):
        '''
        Show settings dialog
        '''
        window = SettingsView(self.save_settings, self.restore_default_settings, self.reset_cache, self.zcore)
        
        self.init_menu(window)
        self.program.add_window(window)
        window.show_all()
        
    def reset_cache(self):
        '''
        remove any cached data
        '''
        self._call_handled_method(self._reset_cache)
        
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
      
       
    def refresh_from_menu(self, widget, data):
        self._call_handled_method(self._refresh_from_menu)
       
    def show_network_news_from_menu(self, widget, data):
        self.show_network_news()
       
    def show_note_information(self, mess):
       parent = hildon.WindowStack.get_default().peek()
       note = hildon.hildon_note_new_information(parent,mess)                 
   
       response = gtk.Dialog.run(note)

    def show_banner_information(self, mess):
       parent = hildon.WindowStack.get_default().peek()
       banner= hildon.hildon_banner_show_information(parent,"", mess)
       banner.set_timeout(2000) 
    
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
        self.show_network_news()                            
       
       

   

    def show_network_news(self):
        '''
        ZouriteGui always display the network news as main view.
        '''
        # Create the home view        
        window = NetworkNewsView(self.update_network_news, self.select_an_update_network_new, self.show_update_status, self.show_post_news)        
        window.set_title("Network news")
        self.init_menu(window)
        self.program.add_window(window)
        window.show_all()
                
       

   
    def update_network_news(self, view):
        '''
        callback function invoked by the NetworkNewsView when it want
        to be refreshed
        view is the NetworkNewsView
        '''
        self._call_handled_method(self._update_network_news,view)
        
        
    def show_update_status(self, widget, view):
        # TODO this method must be called by the NetworkNewsView not by gtk loop
        # in order to avoid theses extra unused parameter
        self._call_handled_method(self._show_update_status)
        
            
    
    
    def modify_status(self, status):
        '''
        callback funtion to modify the user status
        '''
        self._call_handled_method(self._modify_status,status)
            
        
        
    def clear_status(self):
        '''
        callback funtion to modify the user status
        '''
        self._call_handled_method(self._clear_status)
            
    
    def show_post_news(self, widget, view):
        '''
        Show a view to edit the message to post
        '''
        window = NewsMessageEditorView(self.send_message_to_network)
        
        
        self.init_menu(window)
           
        self.program.add_window(window)
        window.show_all()
        
    def send_message_to_network(self, message):
        '''
        Send the message and close the current view
        '''
        self._call_handled_method(self._send_message_to_network,message)
    
    def show_detail_profil(self, widget, shortProfile):
        '''
        A Windows call us to display the full profile for the given short profile
        '''
        self._call_handled_method(self._show_detail_profil,shortProfile)

    
    def place_call(self, person):
        '''
        Initiate a phone call to the given ShortProfile.
        '''
        # this launch a call so we must have aggreement of the user
        message = "Do you want to call " + person.firstname + " " + person.lastname + " at " + person.phone
        parent = hildon.WindowStack.get_default().peek()
        note = hildon.hildon_note_new_confirmation(parent, message)
   
        response = gtk.Dialog.run(note)
   
        note.destroy()
        
        if response == gtk.RESPONSE_OK:        
                       
            bus = dbus.SystemBus()
            csd_call = dbus.Interface(bus.get_object('com.nokia.csd',
                                                     '/com/nokia/csd/call'),
                                                     'com.nokia.csd.Call')
            csd_call.CreateWith(person.phone, dbus.UInt32(0))
            self.show_banner_information("call in progress")
        else:
            self.show_banner_information("call cancelled")
        
            
        

    def place_email(self, person):
        '''
        Initiate a mail editor to create a message to the given ShortProfile
        '''
        bus = dbus.SystemBus()
        csd_call = dbus.Interface(bus.get_object('com.nokia.modest',
                                            '/com/nokia/modest'),
                                            'com.nokia.modest')
        csd_call.MailTo("mailto:" + person.email)
    
    
    def show_invite_profile(self, widget, shortProfile):
        '''
        The widget call us to invite the given profile
        '''        
        window = MessageEditorView(shortProfile, self.send_request_invite_profile)
        
        
        self.init_menu(window)
           
        self.program.add_window(window)
        window.show_all()
        
    def show_message_profile(self, widget, shortProfile):
        '''
        The widget call us to message the given profile
        '''
        
        window = MessageEditorView(shortProfile, self.send_message_to_profile)
        
        
        self.init_menu(window)
           
        self.program.add_window(window)
        window.show_all()
    
    def send_message_to_profile(self, profile, subject, body):
        '''
        The send bouton of the view MessageEditorView has been clicked.
        Our job i snow to send the message ! 
        '''       
        self._call_handled_method(self._send_message_to_profile,profile, subject, body)

    
    def send_request_invite_profile(self, profile, subject, body):
        '''
        The send bouton of the view MessageEditorView has been clicked.
        Our job is now to send the invitation !
        '''
        self._call_handled_method(self._send_request_invite_profile,profile, subject, body)
    
    def select_an_update_network_new(self, netUpdateConn):
        '''
        The user has selected a network update news. We have to show the detail now.
        '''
        # Create the news news detail
        
       
        if isinstance(netUpdateConn, plugin.NetworkUpdateSelfConnection) :     
            self.show_network_update_self_connection_detail(netUpdateConn)
                            
        elif isinstance(netUpdateConn, plugin.NetworkUpdateConnection) :
            self.show_network_update_connection_detail(netUpdateConn)
        else:
            self.show_note_information("the type " + str(netUpdateConn.type) + " is not supported yet")            
        
        # This call show the window and also add the window to the stack
        
    
    def show_network_update_connection_detail(self, netUpdateConn):
        '''
        SHow the detail of a network update connection 
        '''
        self._call_handled_method(self._show_network_update_connection_detail,netUpdateConn)
     
    def show_network_update_self_connection_detail(self, netUpdateConn):
        '''
        SHow the detail of a network update connection 
        '''
        self._call_handled_method(self._show_network_update_self_connection_detail,netUpdateConn)
   
     
    
    def run(self):
        # the splash screen  is displayed,now show the home screen in a fancy tansition               
        gtk.main()


        

class ZouriteStackableWindow(hildon.StackableWindow):
    '''
    general design of any GUI of this app
    '''
    
    centerview = None;
    bottomButtons = None;
    
    def __init__(self, title="Zourite"):
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

class AboutView(ZouriteStackableWindow):
    '''
    This view show a fancy about dialog
    '''

    def init_center_view(self, centerview):
        
        pixbuf = gtk.gdk.pixbuf_new_from_file("zourite-logo.png")
        image = gtk.Image()
        image.set_from_pixbuf(pixbuf)
        centerview.add(image)
        
        centerview.add(gtk.Label("ZOURITE - " + version.getInstance().getVersion()))
        centerview.add(gtk.Label("Professional networking application for N900"))
        centerview.add(gtk.Label("by Thierry Bressure - http://blog.zourite.bressure.net"))


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
         webbrowser.open_new_tab("http://blog.zourite.bressure.net");
    
    def on_site_clicked_event(self, widget, data):
         webbrowser.open_new_tab("http://zourite.bressure.net");
         
    def on_group_clicked_event(self, widget, data):
         webbrowser.open_new_tab("http://group.zourite.bressure.net");
             
    

class SplashScreenView(ZouriteStackableWindow):
    '''
    This is the first view of the application e.g. the main view.  
    '''

    def init_center_view(self, centerview):
        pixbuf = gtk.gdk.pixbuf_new_from_file("zourite-logo.png")
        for i in range(1,4):
            hbox = gtk.HBox()
            for j in range(1,5):                
                image = gtk.Image()
                image.set_from_pixbuf(pixbuf)
                hbox.add(image)
            centerview.add(hbox)


class BugReportView(ZouriteStackableWindow):
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
        ZouriteStackableWindow.__init__(self, title="Bug reporting") 

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
        return ZouriteStackableWindow.init_center_view(self, centerview)


    def init_bottom_button(self, bottomButtons):
        post = self.create_button("Post issue", None)
        post.connect("clicked", self.on_post_button_clicked, self)
        self.add_button(post)                     
        return ZouriteStackableWindow.init_bottom_button(self, bottomButtons)

    def on_post_button_clicked(self, widget, view):
        buffer = view._body.get_buffer()
        body = buffer.get_text(buffer.get_start_iter(), buffer.get_end_iter())
        subject =  view._subject.get_text()
        self.submit_issue_callback(subject, body)
        




class ContactListView(ZouriteStackableWindow):
    '''
    View to browse all contact
    '''
    
    def __init__(self, select_contact_callback, phone_call_callback, email_callback, zcore):
        self.zcore= zcore        
        self.select_contact_callback = select_contact_callback
        self.phone_call_callback = phone_call_callback            
        self.email_callback = email_callback
        
        self.email_pixbuf = gtk.gdk.pixbuf_new_from_file("email_message_editor.png")
        self.email_pixbuf_disabled = self.email_pixbuf.copy()
        self.email_pixbuf_disabled.saturate_and_pixelate(self.email_pixbuf_disabled, 0.3, False)   
        
        self.call_pixbuf = gtk.gdk.pixbuf_new_from_file("general_call.png")
        self.call_pixbuf_disabeld = self.call_pixbuf.copy()
        self.call_pixbuf_disabeld.saturate_and_pixelate(self.call_pixbuf_disabeld, 0.3, False)
        
        # TODO create a list of contact
        ZouriteStackableWindow.__init__(self, "Contacts list")

    def init_center_view(self, centerview):
        
        self.model = gtk.ListStore(gtk.gdk.Pixbuf, str, str,gtk.gdk.Pixbuf, gtk.gdk.Pixbuf,object)
        # sort on contacts name
        self.model.set_sort_column_id(1,gtk.SORT_ASCENDING)
        
        self.refresh()
         # create the view
        self.view = gtk.TreeView(self.model)
        
        picture_column = gtk.TreeViewColumn("picture")
        picture_column_renderer = gtk.CellRendererPixbuf()
        picture_column.pack_start(picture_column_renderer)
        picture_column.set_attributes(picture_column_renderer, pixbuf=0) 
        self.view.append_column(picture_column)
        
        contact_column = gtk.TreeViewColumn("contact")
        contact_column.set_property("sizing", gtk.TREE_VIEW_COLUMN_FIXED)
        contact_column.set_property("fixed-width", 300)
        contact_column_renderer = gtk.CellRendererText()
        contact_column.pack_start(contact_column_renderer)
        contact_column.set_attributes(contact_column_renderer, text=1)
        self.view.append_column(contact_column)

        headline_column = gtk.TreeViewColumn("headline")
        headline_column.set_property("sizing", gtk.TREE_VIEW_COLUMN_FIXED)
        headline_column.set_property("fixed-width", 300)       
        renderer_txt = gtk.CellRendererText()
        renderer_txt.set_property("size-points",10)
        headline_column.pack_start(renderer_txt)
        headline_column.set_attributes(renderer_txt, text=2)
        self.view.append_column(headline_column)

        emailcolumn = gtk.TreeViewColumn("email")            
        emailcolumn_renderer = gtk.CellRendererPixbuf()
        emailcolumn.pack_start(emailcolumn_renderer)
        emailcolumn.set_attributes(emailcolumn_renderer, pixbuf=3) 
        self.view.append_column(emailcolumn)
        
        callcolumn = gtk.TreeViewColumn("call")            
        callcolumn_renderer = gtk.CellRendererPixbuf()
        callcolumn.pack_start(callcolumn_renderer)
        callcolumn.set_attributes(callcolumn_renderer, pixbuf=4) 
        self.view.append_column(callcolumn)

        self.view.connect("row-activated", self.on_contact_row_activated, None)
        

        
        
        centerview.add(self.view)
        

    def on_contact_row_activated(self,  treeview, path, view_column,  user_data):
        store = treeview.get_model()
        iter = store.get_iter(path)
        person, = store.get(iter,5)
        # check if the activation come from a nice icon
        title = view_column.get_property('title')
        if  title == "call" and person.phone is not None:
             self.phone_call_callback(person)
        elif title == "email" and person.email is not None:
             self.email_callback(person)
        else:            
            self.select_contact_callback(person)

 
        

    def init_bottom_button(self, bottomButtons):
        return ZouriteStackableWindow.init_bottom_button(self, bottomButtons)

    def refresh(self):
        '''
        this view is asked to reresh itself with latest data.
        the refresh function is defined at instanciation
        '''
        peopleList = self.zcore.getMyConnections()
        self.model.clear()
        
        # simply push all data in the model            
        for people in peopleList:
                contact = people.lastname.upper() + " " + people.firstname.capitalize()
                headline = people.headline
                                
                if people.email is None:
                    emailPict = self.email_pixbuf_disabled
                else:
                    emailPict = self.email_pixbuf
                if people.phone is None:
                    phonePict = self.call_pixbuf_disabeld
                else:
                    phonePict = self.call_pixbuf
                    
                self.model.append([self.zcore.getGtkPixBufForProfile(people).scale_simple(80,80,gtk.gdk.INTERP_BILINEAR) , 
                                   contact, headline, 
                                   emailPict,
                                   phonePict
                                   , people])
        
       

class SettingsView(ZouriteStackableWindow):
    '''
    View to manage settings of the application.
    '''
    
    def __init__(self, save_callback, default_callback, reset_cache_callback, zcore):        
        self.zcore = zcore
        self.save_callback = save_callback
        self.default_callback = default_callback
        self.reset_cache_callback = reset_cache_callback
        self.gtkWidgetForPluginConf = {}
        ZouriteStackableWindow.__init__(self, "Settings")

    def _create_config_plugin_page(self, notebook, current_page_number):
        
        #todo change the notebook
        nextPage = gtk.VBox()
        # print current value
        keys = self.pluginConfData.keys()
        if plugin.PLUGIN_CONF_INFO in keys:
            nextPage.add(gtk.Label(self.pluginConfData[plugin.PLUGIN_CONF_INFO]))
        
        if plugin.PLUGIN_CONF_WEBBROWSER in keys:
            url = self.pluginConfData[plugin.PLUGIN_CONF_WEBBROWSER]
            nextPage.add(gtk.Label("please visit " + url))
            webbrowser.open_new_tab(url)
        
        self.gtkWidgetForPluginConf.clear()
        for key in keys:
        # handle special parameter
            if not key.startswith("__"):
                # standar parameter
                if self.pluginConfData[key] is None:
                    entry = hildon.Entry(gtk.HILDON_SIZE_AUTO_WIDTH)
                    self.gtkWidgetForPluginConf[key]=entry                    
                    caption = hildon.Caption(None, key, entry, None, hildon.CAPTION_MANDATORY)
                    nextPage.add(caption)
                
            
        
        notebook.insert_page(nextPage, position=current_page_number+1)


    def init_center_view(self, centerview):
        
        cacheSettings = gtk.HBox()
        
        cachePickerBtn =  hildon.PickerButton(gtk.HILDON_SIZE_AUTO , hildon.BUTTON_ARRANGEMENT_VERTICAL)
        cachePickerBtn.set_title("cache strategy")
        self.strategySelector = self.create_cache_strategy_selector()
        cachePickerBtn.set_selector(self.strategySelector)
        cacheSettings.add(cachePickerBtn)
             
        
        storePickerBtn =  hildon.PickerButton(gtk.HILDON_SIZE_AUTO , hildon.BUTTON_ARRANGEMENT_VERTICAL)
        storePickerBtn.set_title("cache store")
        self.storeSelector = self.create_cache_store_selector()
        storePickerBtn.set_selector(self.storeSelector)
        cacheSettings.add(storePickerBtn)
        
        centerview.add(cacheSettings)         
        
        resetCacheBtn = hildon.Button(gtk.HILDON_SIZE_FINGER_HEIGHT, hildon.BUTTON_ARRANGEMENT_HORIZONTAL, "clear cache", None)
        resetCacheBtn.connect("clicked", self.on_reset_cache_clicked_event, None)
        centerview.pack_start(resetCacheBtn, False, False, 0)
                
        pluginPickerBtn =  hildon.PickerButton(gtk.HILDON_SIZE_AUTO , hildon.BUTTON_ARRANGEMENT_VERTICAL)
        pluginPickerBtn.set_title("network")
        self.pluginSelector = self.create_plugin_selector()
        pluginPickerBtn.set_selector(self.pluginSelector)
        centerview.add(pluginPickerBtn)       
        
        plugigConfButton = hildon.Button(gtk.HILDON_SIZE_FINGER_HEIGHT, hildon.BUTTON_ARRANGEMENT_HORIZONTAL, "configure", None)
        plugigConfButton.connect("clicked", self.on_configure_plugin_clicked_event, None)
        centerview.pack_start(plugigConfButton, False, False, 0)
        
        
    def on_configure_plugin_clicked_event(self, widget, data):
        '''
        Open a dialog to choose the plugin to configure
        '''        
        self.gtkWidgetForPluginConf.clear()     
        
        notebook = gtk.Notebook()
        
        welcome = gtk.Label("This wizzard will help you to configure a plugin")        
        plugin_selector = self.create_plugin_selector_for_configuration()
        finish  = gtk.Label("The plugin is successfuly configured")
        
        notebook.append_page(welcome)
        notebook.append_page(plugin_selector,gtk.Label("select plugin"))
        notebook.append_page(finish)
        
        dialog = hildon.WizardDialog(self, "Plugin Configuration", notebook)
   
        # Set a handler for "switch-page" signal
        notebook.connect("switch-page", self.on_page_switch, dialog)
        notebook.connect("change-current-page", self.on_current_page_change, dialog)
        notebook.connect("page-added", self.on_page_added, dialog)
   
        # Set a function to decide if user can go to next page
        dialog.set_forward_page_func(self.some_page_func)
   
        dialog.show_all()
        response = dialog.run()
        dialog.destroy()
        
        self.gtkWidgetForPluginConf.clear()
        
    
    def  on_page_added(self, notebook, child, page_num, dialog):
        print >>sys.stderr, "page added num %d" % page_num               
        dialog.show_all()

    def on_current_page_change(self, notebook, offset, dialog):
        print >>sys.stderr, "current page change offset %d" % offset
        
    def on_page_switch(self, notebook, page, num, dialog):
       print >>sys.stderr, "Page swith %s %d" % (str(page), num)
       return True
   
    def some_page_func(self, notebook, current_page_number, userdata):   
        print >>sys.stderr, "check forward page for page " + str(current_page_number)
        if current_page_number == 0 :
            return True
        elif current_page_number == 1 :
            # must have choose a plugin
            plugin_selector = notebook.get_nth_page(current_page_number)            
            selectedRows = plugin_selector.get_selected_rows(0)
            if len(selectedRows) == 1 :
                # start the plugin configuration
                plugPath = selectedRows[0]
                plugModel =  plugin_selector.get_model(0)
                plugIter = plugModel.get_iter(plugPath)
                plugid, = plugModel.get(plugIter,0)                
                self.pluginConf = self.zcore.getPluginAmongAvailable(plugid)
                self.pluginConfData = self.pluginConf.configure()   
                self._create_config_plugin_page(notebook, current_page_number)
                notebook.next_page()
                return False
            else:
                # cannot jump to next page without selecting one plugin to configure
                return False
        else:
            # does the plugin expect some data ?
            if len(self.pluginConfData) > 0:
                # provide the data to the plugin
                
                for key in self.gtkWidgetForPluginConf.keys():
                    entry = self.gtkWidgetForPluginConf[key]
                    self.pluginConfData[key] = entry.get_text()
                self.gtkWidgetForPluginConf.clear()    
                self.pluginConfData = self.pluginConf.configure(self.pluginConfData)
                # prepare the next page if required by the plugin
                if len(self.pluginConfData) > 0:
                    self._create_config_plugin_page(notebook, current_page_number)
                    notebook.next_page()
                    return False
                else :
                    return True                    
            else:
                # no more data required by the plugin
                return True
            

    
    def on_reset_cache_clicked_event(self, widget, data):
        message = "This will remove all local data from your network. Are you sur?"
        parent = hildon.WindowStack.get_default().peek()
        note = hildon.hildon_note_new_confirmation(parent, message)
   
        response = gtk.Dialog.run(note)
   
        note.destroy()
        
        if response == gtk.RESPONSE_OK:
            self.reset_cache_callback()      
    
    
    def create_plugin_selector_for_configuration(self):
        #Create a HildonTouchSelector with a single text column
        selector = hildon.TouchSelector(text = True)
        # Populate selector    
        pluginPathList = self.pluginSelector.get_selected_rows(0)
        pluginModel = self.pluginSelector.get_model(0)
        
        for path in pluginPathList:
                    
            pluginIter = pluginModel.get_iter(path)
            pluginId, = pluginModel.get(pluginIter,0)            
            selector.append_text(pluginId)

        return selector
    
    
    def create_plugin_selector(self):
        #Create a HildonTouchSelector with a single text column
        selector = hildon.TouchSelector(text = True)
        # Set selection mode to allow multiple selection
        selector.set_column_selection_mode(hildon.TOUCH_SELECTOR_SELECTION_MODE_MULTIPLE)  
        registeredPlugin = self.zcore.getRegisteredPlugin()
        registered_plugin_id_list = map(lambda(x): x.get_plugin_id(),registeredPlugin)
        # Populate selector
        rang = -1
        for plugin in self.zcore.getAvailablePlugins():
            rang = rang + 1
            label = plugin.get_plugin_id() # TODO replace by a user friendly label
            # Add item to the column
            selector.append_text(label)
            # must this be selected ?
            plugin_id = plugin.get_plugin_id()
             
            if plugin_id in registered_plugin_id_list:
                selector.select_iter(0, selector.get_model(0).get_iter(rang), False)
        
    
        
        return selector
    
    
    def create_cache_strategy_selector(self):
        #Create a HildonTouchSelector with a single text column
        selector = hildon.TouchSelector(text = True)
    
        currentCacheStrategy = self.zcore.getCurrentCacheStrategy()
        
        # Populate selector
        rang = -1
        for strategy in self.zcore.getAvailableCacheStrategies():
            rang = rang + 1
            label = strategy # TODO replace by a user friendly label
            # Add item to the column
            selector.append_text(label)
            if strategy == currentCacheStrategy :
                selector.select_iter(0,selector.get_model(0).get_iter(rang), False)
    
        # Set selection mode to allow multiple selection
        selector.set_column_selection_mode(hildon.TOUCH_SELECTOR_SELECTION_MODE_SINGLE)
    
        return selector
    
    
    
    def create_cache_store_selector(self):
        #Create a HildonTouchSelector with a single text column
        selector = hildon.TouchSelector(text = True)
    
        currentCacheStore = self.zcore.getCurrentCacheStorage()
        
        # Populate selector
        rang = -1
        for store in self.zcore.getAvailableCacheStore():
            rang = rang + 1
            label = store  # TODO replace by a user friendly label
            # Add item to the column
            selector.append_text(label)
            if store == currentCacheStore :
                selector.select_iter(0,selector.get_model(0).get_iter(rang), False)
    
        # Set selection mode to allow multiple selection
        selector.set_column_selection_mode(hildon.TOUCH_SELECTOR_SELECTION_MODE_SINGLE)
    
        return selector
    
   

    def init_bottom_button(self, bottomButtons):
        saveBtn = self.create_button("Save")
        saveBtn.connect("clicked", self.on_save_clicked, self)
        self.add_button(saveBtn)
        defaultBtn = self.create_button("Default")
        defaultBtn.connect("clicked", self.on_default_clicked, self)
        self.add_button(defaultBtn)
      
    def on_save_clicked(self, widget, data):
        settings = zourite.Settings()
        
        stratPath = self.strategySelector.get_selected_rows(0)[0]
        stratModel =  self.strategySelector.get_model(0)
        stratIter = stratModel.get_iter(stratPath)
        settings.cache_strategy, = stratModel.get(stratIter,0)
        
        storePath = self.storeSelector.get_selected_rows(0)[0]
        storeModel =  self.storeSelector.get_model(0)
        storeIter = storeModel.get_iter(storePath)
        settings.cache_storage, = storeModel.get(storeIter,0)
        
        pluginPathList = self.pluginSelector.get_selected_rows(0)
        pluginModel = self.pluginSelector.get_model(0)
        for path in pluginPathList:
           
            pluginIter = pluginModel.get_iter(path)
            pluginId, = pluginModel.get(pluginIter,0)
            settings.registered_plugin_ids.append(pluginId)
        
        self.save_callback(settings)

    def on_default_clicked(self, widget, data):
        self.default_callback()
    

class UpdateStatusView(ZouriteStackableWindow):
    '''
    View used to update the user statuzs status
    '''
    modify_status_callback = None
    clear_status_callback = None
    statusEntry = None
    def __init__(self, currentStatus, modify_status_callback, clear_status_callback):
        '''
        currentStatus a set of current status
        '''
        self.currentStatus = currentStatus
        self.modify_status_callback = modify_status_callback
        self.clear_status_callback = clear_status_callback
        
        ZouriteStackableWindow.__init__(self, "Status")

    def init_center_view(self, centerview):
        
        tableView = gtk.Table(2, 2, True)
                
        tableView.attach(self.justifyRight(gtk.Label("Current status")),0,1,0,1, xpadding=5)
        # construct a status
        statusStr = ""
        for status in self.currentStatus:
            if len(statusStr) > 0:
                statusStr = statusStr + " "
            statusStr = statusStr + status
        if len(statusStr) == 0:
            statusStr = "no status defined"
        tableView.attach(self.justifyLeft(gtk.Label(statusStr)),1,2,0,1)
        tableView.attach(self.justifyRight(gtk.Label("New status")),0,1,1,2, xpadding=5)
        self.statusEntry = hildon.Entry(gtk.HILDON_SIZE_HALFSCREEN_WIDTH)
        tableView.attach(self.justifyLeft(self.statusEntry),1,2,1,2)        
        
        centerview.add(tableView)


    def init_bottom_button(self, bottomButtons):
        modifyBtn = self.create_button("Modify status")
        modifyBtn.connect("clicked", self.on_modify_button_clicked, self.statusEntry)
        self.add_button(modifyBtn)
        clearBtn = self.create_button("Clear status")
        clearBtn.connect("clicked", self.on_clear_button_clicked, None)
        self.add_button(clearBtn)
        
    def on_modify_button_clicked(self, widget, entry):
        self.modify_status_callback(entry.get_text())
    
    def on_clear_button_clicked(self, widget, data):
        self.clear_status_callback()
        

    def justifyLeft(self, widget):
          leftAlign = gtk.Alignment(0,0.5,0,0)
          leftAlign.add(widget)
          return leftAlign

    def justifyRight(self, widget):
          leftAlign = gtk.Alignment(1,0.5,0,0)
          leftAlign.add(widget)
          return leftAlign


    
class NewsMessageEditorView(ZouriteStackableWindow):
    '''
    View used to edit a news message for all connections in my network
    '''
    
    body = None  
    
    def __init__(self, on_send_bouton_clicked_callback):
    
        self.on_send_bouton_clicked_callback = on_send_bouton_clicked_callback
        ZouriteStackableWindow.__init__(self, title = "Edit a message")        
                

    def init_bottom_button(self,  hbox):
        sendBtn = self.create_button("Send")
        sendBtn.connect("clicked", self.on_send_bouton_clicked, self.body)
        self.add_button(sendBtn)
        
    def on_send_bouton_clicked(self, widget, textView):
        buffer = textView.get_buffer()
        body = buffer.get_text(buffer.get_start_iter(), buffer.get_end_iter())
        self.on_send_bouton_clicked_callback(body)

    def init_center_view(self, centerview):
        
        # create the content of the cneter view
      
        contentLbl = gtk.Label("Content")
        centerview.pack_start(self.justifyLeft(contentLbl), False)
        self.body = hildon.TextView()
        self.body.set_placeholder("enter the message here")
        self.body.set_wrap_mode(gtk.WRAP_WORD)
        centerview.add(self.body)

            

class MessageEditorView(ZouriteStackableWindow):
    '''
    View used to edit a message
    '''
    
    subject = None
    body = None
    profile = None
    
    def __init__(self, shortProfile, send_bouton_callback):
        self.profile = shortProfile
        self.send_bouton_callback = send_bouton_callback
        ZouriteStackableWindow.__init__(self, title = "Edit a message")        
                

    def init_bottom_button(self,  hbox):
        sendBtn = self.create_button("Send")
        sendBtn.connect("clicked", self.on_send_button_clicked, self)
        self.add_button(sendBtn)

    def on_send_button_clicked(self, widget, view):
        buffer = view.body.get_buffer()
        body = buffer.get_text(buffer.get_start_iter(), buffer.get_end_iter())
        subject =  view.subject.get_text()
        self.send_bouton_callback(self.profile, subject, body)

    def init_center_view(self, centerview):
        
        # create the content of the cneter view
        subjectLbl = gtk.Label("Subject")
        centerview.pack_start(self.justifyLeft(subjectLbl), False)
        self.subject = hildon.Entry(gtk.HILDON_SIZE_FULLSCREEN_WIDTH)
        self.subject.set_placeholder("enter a subject")
        centerview.pack_start(self.subject, False)
        contentLbl = gtk.Label("Content")
        centerview.pack_start(self.justifyLeft(contentLbl), False)
        self.body = hildon.TextView()
        self.body.set_placeholder("enter the message here")
        self.body.set_wrap_mode(gtk.WRAP_WORD)
        centerview.add(self.body)

         
   


class FullProfileView(ZouriteStackableWindow):
    '''
    View showing the detail of a profile e.g full profile
    '''        
    def __init__(self, fullProfile, on_invite_button_clicked, on_message_button_clicked,  zcore):
        
        self.fullProfile = fullProfile
        self.on_invite_button_clicked = on_invite_button_clicked
        self.on_message_button_clicked = on_message_button_clicked
        self.zcore = zcore
        
        ZouriteStackableWindow.__init__(self, title = "Profile detail")        
    
     
    def init_bottom_button(self,  hbox):
        
        # TODO if profile is part of connection we can send him a message        
        # otherwose we should invite him
        messageBtn = self.create_button( "Send a message")
        messageBtn.connect("clicked", self.on_message_button_clicked, self.fullProfile)
        self.add_button(messageBtn)
        inviteBtn = self.create_button("Invite")
        inviteBtn.connect("clicked", self.on_invite_button_clicked, self.fullProfile)
        self.add_button(inviteBtn)


    def init_center_view(self, centerview ):
        centerview.set_spacing(5)
        # add the header
        header = self.create_header(self.fullProfile, self.zcore)
        centerview.pack_start(header, False)
        # add the summary
        summary = gtk.Label(self.fullProfile.summary)
        summary.set_line_wrap(True)
        frame = gtk.Frame("summary")
        frame.add(summary)
        centerview.pack_start(frame)
        # add the positions
        for position in self.fullProfile.positions:
            frame = gtk.Frame(position.title + " at " + position.company)
            if position.dateDebut is None:
                datePosition = ""
            else :
                datePosition = str(position.dateDebut)
            summary = gtk.Label("from " + datePosition + " : " + position.summary)
            summary.set_line_wrap(True)
            frame.add(summary)
            centerview.pack_start(frame)
        
        return centerview


    
        
    def create_header(self, fullProfile, zcore):
        header = gtk.HBox()
        image = zcore.getGtkImageForProfile(fullProfile)
        header.pack_start(image)
        description = gtk.VBox()       
        description.pack_start(self.justifyLeft(gtk.Label(fullProfile.lastname.upper())))
        description.pack_start(self.justifyLeft(gtk.Label(fullProfile.firstname.capitalize())))
        description.pack_start(self.justifyLeft(gtk.Label(fullProfile.headline)))
        description.pack_start(self.justifyLeft(gtk.Label(fullProfile.industry)))
        header.pack_start(description)
        return header
    
    def justifyLeft(self, widget):
          leftAlign = gtk.Alignment(0,0,0,0)
          leftAlign.add(widget)
          return leftAlign

class NetworkUpdateConnectionView(ZouriteStackableWindow):
    '''
    View showing an update connection details
    '''    
    def __init__(self, myConnShortProfile, newConnShortProfile, on_detail_profil_request, on_invite_bouton_clicked, zcore):
        
        self.myConnShortProfile = myConnShortProfile
        self.newConnShortProfile = newConnShortProfile
        self.on_detail_profil_request = on_detail_profil_request
        self.on_invite_bouton_clicked = on_invite_bouton_clicked
        self.zcore = zcore
        
        ZouriteStackableWindow.__init__(self, title = "New connection update")      
        
      
    def init_bottom_button(self, hbox):
        self.add_button(self.create_button("Make a comment"))
        inviteBtn = self.create_button( "Invite")
        inviteBtn.connect("clicked", self.on_invite_bouton_clicked, self.newConnShortProfile)
        self.add_button(inviteBtn)
       


    def init_center_view(self,  centerview):
        tableView = gtk.Table(3, 3, False)
        myconn_pict, myconn_name, myconn_lbl = self.create_shortProfile(self.myConnShortProfile, self.on_detail_profil_request, self.zcore)
        centralVBox = gtk.VBox()
        centralVBox.pack_start(gtk.Label("is now connected to"))
        newconn_pict, newconn_name, newconn_lbl = self.create_shortProfile(self.newConnShortProfile, self.on_detail_profil_request, self.zcore)
        tableView.attach(myconn_pict, 0, 1, 0, 1, xoptions=gtk.EXPAND, yoptions=gtk.SHRINK)
        tableView.attach(myconn_name, 0, 1, 1, 2)
        tableView.attach(myconn_lbl, 0, 1, 2, 3)
        tableView.attach(centralVBox, 1, 2, 0, 3, xoptions=gtk.EXPAND, yoptions=gtk.SHRINK | gtk.EXPAND)
        tableView.attach(newconn_pict, 2, 3, 0, 1, xoptions=gtk.EXPAND, yoptions=gtk.SHRINK)
        tableView.attach(newconn_name, 2, 3, 1, 2)
        tableView.attach(newconn_lbl, 2, 3, 2, 3)
        centerview.add(tableView)

        
    def create_shortProfile(self, shortProfile, on_detail_profil_request, zcore):
            
        
        
        picture = zcore.getGtkImageForProfile(shortProfile)
        pictAlign = gtk.Alignment(0.5,0.5,0,0)
        pictAlign.add(picture)
            
            
            
        nameButton = hildon.Button(gtk.HILDON_SIZE_FINGER_HEIGHT| gtk.HILDON_SIZE_AUTO_WIDTH , hildon.BUTTON_ARRANGEMENT_VERTICAL,shortProfile.firstname, shortProfile.lastname)
        nameButton.connect("clicked",on_detail_profil_request, shortProfile) 
        nameAlign = gtk.Alignment(0.5,0,0,0)
        nameAlign.add(nameButton)
            
            
        label = gtk.Label(shortProfile.headline)   
        label.set_single_line_mode(False)                
        label.set_max_width_chars(20)   
        label.set_line_wrap(True) # this does not work :-(
        labelAlign = gtk.Alignment(0.5,0,0,0)               
        labelAlign.add(label)
        
        return pictAlign, nameAlign, labelAlign    
        

class NetworkUpdateSelfConnectionView(ZouriteStackableWindow):
    '''
    View showing a new connection for the current user
    '''
    def __init__(self,  newConnShortProfile, on_detail_profil_request,  zcore):
        
       
        self.newConnShortProfile = newConnShortProfile
        self.on_detail_profil_request = on_detail_profil_request        
        self.zcore = zcore
        
        ZouriteStackableWindow.__init__(self, title = "New connection update")      
        
      
    def init_bottom_button(self, hbox):
        self.add_button(self.create_button("Make a comment"))
      
       


    def init_center_view(self,  centerview):
        centerview.add(gtk.Label("Your are  now connected to"))
        newconn_pict, newconn_name, newconn_lbl = self.create_shortProfile(self.newConnShortProfile, self.on_detail_profil_request, self.zcore)    
        centerview.add(newconn_pict)
        centerview.add(newconn_name)
        centerview.add(newconn_lbl)

        
    def create_shortProfile(self, shortProfile, on_detail_profil_request, zcore):
            
        
        
        picture = zcore.getGtkImageForProfile(shortProfile)
        pictAlign = gtk.Alignment(0.5,0.5,0,0)
        pictAlign.add(picture)
            
            
            
        nameButton = hildon.Button(gtk.HILDON_SIZE_FINGER_HEIGHT| gtk.HILDON_SIZE_AUTO_WIDTH , hildon.BUTTON_ARRANGEMENT_VERTICAL,shortProfile.firstname, shortProfile.lastname)
        nameButton.connect("clicked",on_detail_profil_request, shortProfile) 
        nameAlign = gtk.Alignment(0.5,0,0,0)
        nameAlign.add(nameButton)
            
            
        label = gtk.Label(shortProfile.headline)   
        label.set_single_line_mode(False)                
        label.set_max_width_chars(20)   
        label.set_line_wrap(True) # this does not work :-(
        labelAlign = gtk.Alignment(0.5,0,0,0)               
        labelAlign.add(label)
        
        return pictAlign, nameAlign, labelAlign   


        
class NetworkNewsView(ZouriteStackableWindow):
    
    model = None
    view = None
    refresh_func = None
    select_function = None
    
    def __init__(self, refresh_function, select_function, on_status_bouton_clicked, on_news_bouton_clicked):
        '''
        the refresh function is a pointer on the function which will be called
        when this views need to be updated with fresh data.
        the networkUpdateList is the initial data standing for the model of this list view
        '''
        self.refresh_func = refresh_function
        self.select_function = select_function
        self.on_status_bouton_clicked = on_status_bouton_clicked
        self.on_news_bouton_clicked = on_news_bouton_clicked

        ZouriteStackableWindow.__init__(self, title = "Network news")
    
       
                        

    def init_bottom_button(self, bottomButton):
        statusBtn = self.create_button("Update my status")
        statusBtn.connect("clicked", self.on_status_bouton_clicked, self)
        self.add_button(statusBtn)
        newsBtn = self.create_button("Post news")
        newsBtn.connect("clicked", self.on_news_bouton_clicked, self)
        self.add_button(newsBtn)


    def init_center_view(self, centerview):
        
        # create the model
        self.model = gtk.ListStore(gtk.gdk.Pixbuf, str, object)
        self.refresh()
        # create the view
        self.view = gtk.TreeView(self.model)
        # create the column
        tvcolumnconn = gtk.TreeViewColumn("Connection")
        renderer_pix_conn = gtk.CellRendererPixbuf()
        tvcolumnconn.pack_start(renderer_pix_conn)
        tvcolumnconn.set_attributes(renderer_pix_conn, pixbuf=0) 
        self.view.append_column(tvcolumnconn)
        
        tvcolumntxt = gtk.TreeViewColumn("Network news")
        renderer_txt = gtk.CellRendererText()
        renderer_txt.set_property("size-points", 15)
        tvcolumntxt.pack_start(renderer_txt)
        tvcolumntxt.set_attributes(renderer_txt, text=1)
        self.view.append_column(tvcolumntxt)
       
        
        self.view.connect("row-activated", self.on_row_activated, None)
        centerview.add(self.view)


    def on_row_activated(self, treeview, path, view_column,  user_data):
         # TODO craete the view according to the type on news
        store = treeview.get_model()
        iter = store.get_iter(path)
        netUpdateConn, = store.get(iter,2)
        self.select_function(netUpdateConn)
    
       
    def refresh(self):
        '''
        this view is asked to refresh itself with latest data.
        the refresh function is defined at instanciation
        '''
        self.refresh_func(self)
    
    def update_network_news(self,networkUpdateLst, zcore):
        '''
        update the model of this view to reflect the network news in the list.
        '''
        self.model.clear()
        # simply push all data in the model
        for netUpd in networkUpdateLst:
                self.model.append([zcore.getGtkPixBufForNetwork(netUpd.networkId) ,str(netUpd), netUpd])
                
            

       

