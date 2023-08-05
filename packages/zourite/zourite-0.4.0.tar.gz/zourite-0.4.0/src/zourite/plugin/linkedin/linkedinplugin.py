# -*- encoding: UTF-8 -*-
'''
Created on 3 mars 2010

@author: thierry
'''

from zourite.core import plugin
import linkedin
import pickle
import logging
import gtk
import gtk.gdk
import datetime


from zourite.common import version


version.getInstance().submitRevision("$Revision: 295 $")

PLUGIN_NAME = "linkedin"

class LinkedInPlugin(plugin.ZouritePlugin):

     
    
    
    API_KEY_DEFAULT = '6OR9klefJ2rGAiezhwDMV2nC7t9j43hVaRUpVAGXqA6VxLoxlQgDHHzEyv45TVvr'
    SECRET_KEY_DEFAULT = 'XFh2GArGOKKv4LlJeGF6FO0l0kWTKqLq51DxdGHZxQjBMAAFOZ1sJawiHA62Pa5O'
    
    API_KEY = ''
    SECRET_KEY = ''
    
    li = None;
    access_token = None
    
    
    unavailable = False # the LinkedIn API has raised a general Exception

       
    
 
    
    def retrieve_access_token(self):
        # essaye de charger l'acces token
        try:
            access_token_file = open(plugin.get_plugin_file_location(PLUGIN_NAME,'li_access_token'),'rb');
            access_token = pickle.load(access_token_file)
        except IOError:
            # pas d'acess token on en génère un autre
            raise plugin.ConfigurationRequiredExeption()            

        return access_token;
    
    
    def configure(self, data=None):
        if data is None:
            data = {}
            plugin.ensure_plugin_config_store_exist(PLUGIN_NAME)
            token = self.li.getRequestToken(None);
            data['token'] = token
            url = self.li.getAuthorizeUrl(token);
            data[plugin.PLUGIN_CONF_INFO] = "visit the provided url to authorize Zourite to access your LinkedIn account." \
                                            " LinkedIn will give you a verifierNote the verifier number that Zourite will ask you for." 
            data[plugin.PLUGIN_CONF_WEBBROWSER] = url
            data['verifier'] = None
            data[plugin.PLUGIN_CONF_STEP] = "VERIFIER"
            return data
        
        elif data[plugin.PLUGIN_CONF_STEP] == 'VERIFIER':
            verifier = int(data["verifier"])
            token = data['token']
            access_token = self.li.getAccessToken(token, verifier);
            try:
                access_token_file = open(plugin.get_plugin_file_location(PLUGIN_NAME,'li_access_token'),'wb');
                pickle.dump(access_token,access_token_file)
                access_token_file.close()
            except IOError:
                logging.warning("the access token could not be saved")
            return {}
        else :
            raise plugin.ConfigurationRequiredExeption() # may raise a specific 




    def _tcr_method(self, method, *arg):
        '''
        call a method and catch any LinkedInDomException then translate it
        into the appropriate ZouriteException
        '''
        if ( self.unavailable ) :
            # try to reinit the connection            
            self.li.reinitConnection()   
            self.unavailable = False         
            
        try:
        
            return method(*arg)
        
        except linkedin.LinkedInDomException, domExc:
            # parse the dom 
            statusDom = domExc.errorDom[0].getElementsByTagName("status")
            if len(statusDom) > 0 :
                status = statusDom[0].firstChild.nodeValue
                message = domExc.getDomMessage()
                if status == "401" and message.find("Expired access token") > -1:                    
                    logging.warn("LinkedIn API raised an exception: configuration is required")
                    raise plugin.ConfigurationRequiredExeption()
                elif status == "403" and message.find("Throttle limit") >  -1:
                    logging.warn("LinkedIn API raised an exception: throttle limit reached")
                    raise plugin.UnvailableException()
                else:
                    logging.error("LinkedIn API raised an exception but it contain an unknow status " + status + " or message")
                    raise 
            else:
                logging.error("LinkedIn API raised an exception that " + PLUGIN_NAME + " can't handle because there is no status")
                raise
            
        except linkedin.LinkedInException:
            logging.warning(PLUGIN_NAME + " catch a general exception, mark the service as unvailable")
            self.unavailable = True
            raise plugin.UnvailableException()
  
    #---------------------------------------------------------------------
    #
    # implementation de l'interface ZouritePlugin
    #
    #---------------------------------------------------------------------

    
    def getMyShortProfile(self):
        profileDom = self._tcr_method(lambda:self.li.profile_api.getMyShortProfile(self.access_token))
        profile = self.ShortProfile(profileDom)
        return profile
    
    def getShortProfile(self, contactId):
        profileDom = self._tcr_method(lambda: self.li.profile_api.getShortProfile(contactId, self.access_token))
        
        
        profile = ShortProfile(profileDom)
        return profile
    
    def getFullProfile(self, contactId):        
        profileDom = self._tcr_method(lambda:self.li.profile_api.getFullProfile(contactId, self.access_token))                
        profile = FullProfile(profileDom)
        return profile
    
    def getMyFullProfile(self):
        profileDom = self._tcr_method(lambda:self.li.profile_api.getMyFullProfile(self.access_token))
        profile = FullProfile(profileDom)
        return profile
    
    def getGtkImage(self, shortProfile):
        '''
        return a gtk.Image for the profil
        '''
        
        return shortProfile.getPicture().getGtkImage() # return a pixbuf it's perhaps better
    
    def getGdkPixbuf(self, shortProfile):
        return shortProfile.getPicture().getGdkPixbuf()
    
    
    def getPluginLogoPixbuf(self):
        return gtk.gdk.pixbuf_new_from_file("linkedin.png")
        
    def get_plugin_id(self):
        return PLUGIN_NAME
    
    def run_plugin(self):        
        try:
            api_key_file = open(plugin.get_plugin_file_location(PLUGIN_NAME,'li_api_key'));
            try:
                self.API_KEY = api_key_file.readline();        
            finally:
                api_key_file.close();
            
            secret_key_file = open(plugin.get_plugin_file_location(PLUGIN_NAME,'li_secret_key'));
            try:
                self.SECRET_KEY = secret_key_file.readline();
            finally:
                secret_key_file.close();
        except:
            self.API_KEY = self.API_KEY_DEFAULT
            self.SECRET_KEY = self.SECRET_KEY_DEFAULT
        
        self.li = linkedin.LinkedIn(self.API_KEY, self.SECRET_KEY);
        self.access_token = self.retrieve_access_token()
    
    def getMyConnections(self):
        people = self._tcr_method(self._getMyConnections)
           
        return people

    def getMyStatus(self):
        return self._tcr_method(lambda:self.li.status_api.getMyStatus(self.access_token));

    def setMyStatus(self, status):
        self._tcr_method(lambda:self.li.status_api.setMyStatus(status, self.access_token));
  
    def clearMyStatus(self):
        self._tcr_method(lambda: self.li.status_api.clearMyStatus(self.access_token));
    
    
    def sendInvitationRequest(self, contactId, subject, body):
        # retrieve an auth token: this is specific to linkedin API
        auth_token = ""
        api_std_profile_dom = self.li.profile_api.getApiStandardProfile(contactId, self.access_token)
        hdDomLst = api_std_profile_dom.getElementsByTagName('http-header')
        if len(hdDomLst) > 0:
            name = hdDomLst[0].getElementsByTagName('name')[0].firstChild.nodeValue
            if name == "x-li-auth-token" :
                auth_token = hdDomLst[0].getElementsByTagName('value')[0].firstChild.nodeValue        
        if auth_token == "":
            pass # TODO raise a plugin exception             
        self.li.communication_api.sendInvitation(contactId, subject, body, auth_token, self.access_token)
        
    
    def sendMessageRequest(self, contactId, subject, body):
        # TODO make some HTML escape in subject and body ?
        self._tcr_method(lambda:self.li.communication_api.sendMessage([contactId],subject, body,self.access_token))
        
    def sendMessageToNetwork(self, body):
        self._tcr_method(lambda:self.li.network_api.sendNewsMessage(body, self.access_token))

    def getNetworkUpdate(self):
        network_update = self._tcr_method(self._getNetworkUpdate)
            
        return network_update;

  
    class NetworkUpdateFactory():
        def createNetworkUpdate(self, update):
            '''
            instanciate a NetworkUpdate or subclass according to the provided
            dom update. Return None when the factory canot handle the entwork update
            '''
            networkUpdate = None
            type = update.getElementsByTagName("update-type")[0].firstChild.nodeValue
            if type == 'CONN':
                networkUpdate = NetworkUpdateConnection(update)
            elif type == 'NCON':
                networkUpdate = NetworkUpdateSelfConnection(update)
            elif type == 'STAT':
                networkUpdate = NetworkUpdateStatus(update)
            elif type == 'PROF':
                networkUpdate = NetworkProfileUpdate(update)
            elif type =='JGRP':
                networkUpdate = NetworkJoinGroup(update)
            else:
                logging.warning("the connection type " + type + " is not yet supported")
            return networkUpdate

    def __str__(self):
        return "zourite plugin for the LinkedIn social network"

    def _getNetworkUpdate(self):
        updateDom = self.li.network_api.getNetworkUpdate(self.access_token)
        network_update = []
        nfactory = self.NetworkUpdateFactory()
        for update in updateDom:
            networkUpdate = nfactory.createNetworkUpdate(update)
            if networkUpdate is not None :
                network_update.append(networkUpdate)
        
        return network_update

    def _getMyConnections(self):
        peopleDom = self.li.connections_api.getMyConnections(self.access_token)
        people = []
        for p in peopleDom:
            person = ShortProfile(p)
            people.append(person)
        
        return people


    
class ShortProfile(plugin.ShortProfile):
     '''
     ShortProfile implementation by this plugin
     '''
     def __init__(self, pdom):
         plugin.ShortProfile.__init__(self)
         id = pdom.getElementsByTagName('id')[0].firstChild.nodeValue
         fn = pdom.getElementsByTagName('first-name')[0].firstChild.nodeValue
         ln = pdom.getElementsByTagName('last-name')[0].firstChild.nodeValue
         headline = pdom.getElementsByTagName('headline')[0].firstChild.nodeValue
         pictDomLst = pdom.getElementsByTagName('picture-url')
         # for some people the API don't return the picture even if there is one...
         if len(pictDomLst) > 0: 
             pictureUrl =  pictDomLst[0].firstChild.nodeValue
             self.picture = plugin.ImageProxyUrl(id,PLUGIN_NAME,pictureUrl)
         else:
             self.picture = plugin.ImageProxyNone()
             
         self.id = id
         self.firstname = fn
         self.lastname = ln
         self.headline = headline 
         
      
         
         self.networkId = PLUGIN_NAME

class FullProfile(ShortProfile,plugin.FullProfile):
     '''
     FullProfile implementation by this plugin
     '''
     def __init__(self, pdom):
         plugin.FullProfile.__init__(self)
         ShortProfile.__init__(self, pdom)
         # init full profile attributes
         locdom = pdom.getElementsByTagName('location')
         if len(locdom) > 0:
             self.location = locdom[0].getElementsByTagName('name')[0].firstChild.nodeValue
         inddom =pdom.getElementsByTagName('industry')
         if len(inddom) > 0:
             self.industry = inddom[0].firstChild.nodeValue
         sumdom = pdom.getElementsByTagName('summary')
         if len(sumdom) > 0:
             if sumdom[0].firstChild != None :
                 self.summary = sumdom[0].firstChild.nodeValue
         positions = pdom.getElementsByTagName('positions')
         if len (positions) > 0:
             posdom = positions[0].getElementsByTagName('position')
             for aPos in posdom:
                 position = Position(aPos)
                 self.positions.append(position
                                       )
class Position(plugin.Position):
     '''
     Position implementation by linkedin plugin
     '''
     
     def __init__(self, pdom):
         title = pdom.getElementsByTagName('title')[0].firstChild.nodeValue
         compdom = pdom.getElementsByTagName('company')[0]
         company = compdom.getElementsByTagName('name')[0].firstChild.nodeValue
         startDateLst = pdom.getElementsByTagName('start-date')
         if len(startDateLst) > 0 :
             startDom = startDateLst[0]
             year = startDom.getElementsByTagName('year')[0].firstChild.nodeValue
             month = "1"
             monthDom = startDom.getElementsByTagName('month')
             if len(monthDom) > 0 :
                 month = monthDom[0].firstChild.nodeValue
              
             plugin.Position.__init__(self,title, company, datetime.date(int(year),int(month),1))
         else:
             plugin.Position.__init__(self,title, company)
         
         sumdom = pdom.getElementsByTagName('summary')
         if len(sumdom) > 0:
             aSumDom = sumdom[0]
             # warning this element of the dom can be empty
             if aSumDom.firstChild !=None :
                 self.summary = aSumDom.firstChild.nodeValue
       
                         
class NetworkUpdateConnection(plugin.NetworkUpdateConnection):
     '''
     Network Update of type connection
     '''
     def __init__(self,updateDom):
         
     
         timestamp = updateDom.getElementsByTagName("timestamp")[0].firstChild.nodeValue
       
         updateContent = updateDom.getElementsByTagName("update-content")[0]
         p = updateContent.getElementsByTagName("person")[0];
     

         conn = Person(p);
         cxs = updateContent.getElementsByTagName("connections")[0];
         newp = cxs.getElementsByTagName("person")[0];
         newconn = Person(newp);
         
         # unlike Java super initialization can occure here, 'cause simply a call to a function
     
         plugin.NetworkUpdateConnection.__init__(self, timestamp, conn, newconn, PLUGIN_NAME)
        

class NetworkUpdateSelfConnection(plugin.NetworkUpdateSelfConnection):
     '''
     Network Update of type connection
     '''
     def __init__(self,updateDom):
         
     
         timestamp = updateDom.getElementsByTagName("timestamp")[0].firstChild.nodeValue
       
         updateContent = updateDom.getElementsByTagName("update-content")[0]
         p = updateContent.getElementsByTagName("person")[0];    
         conn = Person(p);         
         
         # unlike Java super initialization can occure here, 'cause simply a call to a function     
         plugin.NetworkUpdateSelfConnection.__init__(self, timestamp, conn, PLUGIN_NAME)
     

class NetworkUpdateStatus(plugin.NetworkUpdateStatus):
    '''
    A contact have update his status    
    '''
    def __init__(self, updateDom):

         timestamp = updateDom.getElementsByTagName("timestamp")[0].firstChild.nodeValue
       
         updateContent = updateDom.getElementsByTagName("update-content")[0]
         p = updateContent.getElementsByTagName("person")[0];    
         connection = Person(p);         
         
         status = None
         statusDom = p.getElementsByTagName("current-status")         
         if len (statusDom) > 0 :
            status = statusDom[0].firstChild.nodeValue
         
         plugin.NetworkUpdateStatus.__init__(self, timestamp, connection, status, PLUGIN_NAME)


class NetworkProfileUpdate(plugin.NetworkProfileUpdate):
    '''
    LinkedInplugin implementation of NetworkProfileUpdate
    '''
    def __init__(self, updateDom):
        timestamp = updateDom.getElementsByTagName("timestamp")[0].firstChild.nodeValue
        updateContent = updateDom.getElementsByTagName("update-content")[0]
        p = updateContent.getElementsByTagName("person")[0];    
        connection = Person(p); 
        plugin.NetworkProfileUpdate.__init__(self, timestamp, connection, PLUGIN_NAME)

class NetworkJoinGroup(plugin.NetworkJoinGroupUpdate):
    '''
    Linkedin implementation of joind group event
    '''
    def __init__(self, updateDom):
        timestamp = updateDom.getElementsByTagName("timestamp")[0].firstChild.nodeValue
        updateContent = updateDom.getElementsByTagName("update-content")[0]
        p = updateContent.getElementsByTagName("person")[0];    
        connection = Person(p); 
        
        groups = updateContent.getElementsByTagName("member-groups")[0]
        group = groups.getElementsByTagName("member-group")[0]
        groupName = group.getElementsByTagName("name")[0].firstChild.nodeValue
        
        plugin.NetworkJoinGroupUpdate.__init__(self, timestamp, connection, PLUGIN_NAME, groupName)
        
class Person(plugin.Person):
     '''
     linkedin implementation of a zourite person
     '''

     def __init__(self, pdom):
         '''
         intanciate a Person or subclass according to the provided
         dom person
         '''
         plugin.Person.__init__(self)
    
         fn = pdom.getElementsByTagName('first-name')[0].firstChild.nodeValue
         ln = pdom.getElementsByTagName('last-name')[0].firstChild.nodeValue
         id = pdom.getElementsByTagName('id')[0].firstChild.nodeValue
         headline = pdom.getElementsByTagName('headline')[0].firstChild.nodeValue
            
         self.id = id
         self.firstname = fn
         self.lastname = ln
         self.headline = headline     
         self.networkId = PLUGIN_NAME
        



if __name__ == "__main__":
    LinkedInPlugin().run_plugin()


