# -*- encoding: UTF-8 -*-

'''
Created on Mar 3, 2010

@author: maemo
'''

import  webbrowser;
import  pickle;
from zourite.core import  zourite, plugin
import  datetime
import  gtk

from zourite.common import version


version.getInstance().submitRevision("$Revision: 105 $")

class Zourite(zourite.Zourite):
    
    mystatus = ""
    
    def __init__(self):
        self.mystatus = "my status"
        self.settings = zourite.Settings()
    
    def get_plugin_by_id(self, networkid):
        return self;
    
    def get_plugin_id(self):
        return "mock_plugin"
    
    def getAvailablePlugins(self):
        return [self]
    
    def getShortProfilesForNetUpdateConnection(self, netUpdateConn):
        p1 = plugin.ShortProfile();
        p1.firstname = netUpdateConn.connection.firstname
        p1.lastname = netUpdateConn.connection.lastname
        p1.headline = netUpdateConn.connection.headline

        p2 = plugin.ShortProfile();
        p2.firstname = netUpdateConn.newConnection.firstname
        p2.lastname = netUpdateConn.newConnection.lastname
        p2.headline = netUpdateConn.newConnection.headline

        
        return p1,p2
    
    def getGtkImageForProfile(self, shortProfile):
         return plugin.ImageProxyNone().getGtkImage()
    
    def getGtkPixBufForPerson(self, persone):
        return plugin.ImageProxyNone().getGdkPixbuf()
    
    def getPluginLogoPixbuf(self):
          return gtk.gdk.pixbuf_new_from_file("linkedin.png")
    
    def getGtkPixBufForProfile(self, sp):
         return plugin.ImageProxyNone().getGdkPixbuf()
    
    def getFullProfile(self, contactId):
        fullProfile = plugin.FullProfile()
        fullProfile.id=contactId
        fullProfile.firstname = "firstane"
        fullProfile.lastname  ="lastname"
        fullProfile.networkId = "linkedin"
        fullProfile.headline = "headline"
        
        fullProfile.summary = "I've spent a lof of time making program  mainly in financial concern " \
        + "but now i work in a open source company and i dare joining an innovative project dealing " \
        + "with difficul subject"
        
        fullProfile.industry="Software"
        
        p = plugin.Position("Software engineer","Company",datetime.date(2000,1,1));
        p.summary = "work on an CRM project"
        
    
        fullProfile.positions = [p]
        
        return fullProfile
        
    def sendInvitationRequest(self, contactId, subject, body):
        pass;
    
    def sendMessageToProfile(self, shortProfile, subject, body):
        pass
    
    def sendMessageToNetwork(self, body):
        pass
    
    def getMyConnections(self):
        allMyConnection = []
        for i in range(10):
            p = plugin.ShortProfile()
    
            p.firstname = "firstname" + str(i)
            p.headline = "headline" + str(i)
            p.id = "ABCD" + str(i)
            p.lastname = "lastname" + str(i)
            p.phone = "0123456789"
            p.email = "zourite@bressure.net"
    
            allMyConnection.append(p)
            
        return allMyConnection
    
    
    def getShortProfile(self,contactId):
        p1 = plugin.ShortProfile();
        p1.firstname = "Jean"
        p1.lastname = "Dupon"
        p1.headline = "Account manager " + str(contactId)

               
        return p1
        
    def getMyStatus(self):
        return self.mystatus
     
    def setMyStatus(self, status):
       self.mystatus = status
       
    def clearMyStatus(self):
        self.mystatus = ""
        
    def getAllMyStatus(self):
        '''
        Return a set of all status grabbed from every network plugin.
        '''
        status = []
        if len(self.mystatus) > 0:
             status.append(self.mystatus)
        return set(status)
        

    def getNetworkUpdate(self): 
        allMyNetworkUpdate = []
        
        for i in range(10):        
            
            
            p1 = plugin.Person()
            p1.firstname = "firstname" + str(i)
            p1.headline = "headline" + str(i)
            p1.id = "ABCD" + str(i)
            p1.lastname = "lastname" + str(i)
           
            
            p2 = plugin.Person()
            p2.firstname = "firstname" + str(i)
            p2.headline = "headline" + str(i)
            p2.id = "ABCD" + str(i)
            p2.lastname = "lastname" + str(i)
           

            netupdate = plugin.NetworkUpdateConnection("12345678", p1,p2,"linkedin")
            allMyNetworkUpdate.append(netupdate)
        
        return allMyNetworkUpdate