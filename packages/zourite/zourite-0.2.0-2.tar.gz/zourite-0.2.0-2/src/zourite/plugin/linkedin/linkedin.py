"""
LinkedIn OAuth Api Access 
Version: 0.3
License: MIT
Author: Max Lynch <max@mendotasoft.com>
Website: http://mendotasoft.com, http://maxlynch.com
Date Released: 11/23/2009

Enjoy!
"""

import hashlib
import httplib
import time
import urllib2
from xml.dom.minidom import parseString
import logging
import socket


import oauth as oauth

from zourite.common import version


version.getInstance().submitRevision("$Revision: 145 $")

class LinkedIn():
    LI_SERVER = "api.linkedin.com"
    LI_API_URL = "https://api.linkedin.com"

    REQUEST_TOKEN_URL = LI_API_URL + "/uas/oauth/requestToken"
    AUTHORIZE_URL = LI_API_URL + "/uas/oauth/authorize"
    ACCESS_TOKEN_URL = LI_API_URL + "/uas/oauth/accessToken"

    status_api = None
    connection_api = None
    network_api = None
    profile_api = None
    communication_api = None


    def __init__(self, api_key, secret_key):
        self.api_key = api_key
        self.secret_key = secret_key
        self.initConnection()
        
        
    def initConnection(self):
       

        self.connection = httplib.HTTPSConnection(self.LI_SERVER)
        self.consumer = oauth.OAuthConsumer(self.api_key, self.secret_key)
        self.sig_method = oauth.OAuthSignatureMethod_HMAC_SHA1()

        self.status_api = StatusApi(self)
        self.connections_api = ConnectionsApi(self)
        self.network_api = NetworkApi(self)
        self.profile_api = ProfileApi(self)
        self.communication_api = CommunicationApi(self)
        
    def reinitConnection(self):
        self.connection.close()
        self.initConnection()

    def getRequestToken(self, callback):
        """
        Get a request token from linkedin
        """
        oauth_consumer_key = self.api_key

        oauth_request = oauth.OAuthRequest.from_consumer_and_token(self.consumer,
            callback=callback,
            http_url=self.REQUEST_TOKEN_URL)
        oauth_request.sign_request(self.sig_method, self.consumer, None)


        self.connection.request(oauth_request.http_method,
            self.REQUEST_TOKEN_URL, headers=oauth_request.to_header())
        response = self.connection.getresponse().read()

        token = oauth.OAuthToken.from_string(response)
        return token

    def getAuthorizeUrl(self, token):
        """
        Get the URL that we can redirect the user to for authorization of our
        application.
        """
        oauth_request = oauth.OAuthRequest.from_token_and_callback(token=token, http_url=self.AUTHORIZE_URL)
        return oauth_request.to_url()

    def getAccessToken(self, token, verifier):
        """
        Using the verifier we obtained through the user's authorization of
        our application, get an access code.

        Note: token is the request token returned from the call to getRequestToken

        @return an OAuthToken object with the access token.  Use it like this:
            token.key -> Key
            token.secret -> Secret Key
        """
        oauth_request = oauth.OAuthRequest.from_consumer_and_token(self.consumer, token=token, verifier=verifier, http_url=self.ACCESS_TOKEN_URL)
        oauth_request.sign_request(self.sig_method, self.consumer, token)

        self.connection.request(oauth_request.http_method, self.ACCESS_TOKEN_URL, headers=oauth_request.to_header())
        response = self.connection.getresponse()
        return oauth.OAuthToken.from_string(response.read())

    """
    More functionality coming soon...
    """

class LinkedInApi():
    def __init__(self, linkedin):
        self.linkedin = linkedin
        
    def _call_and_handle_low_level_error(self, method):
        try:
            method()
        except (socket.error, socket.herror, socket.gaierror, socket.timeout):            
            raise LinkedInException("LinkedIn API : socket connection failed")
        except (httplib.CannotSendRequest):
            raise LinkedInException("LinkedIn API : http communication failed")

    def doApiRequest(self, url, access_token):
        """
        make a call to linkedin and return the dom response.
        some check are done so exception are raised in case of error
        """
        oauth_request = oauth.OAuthRequest.from_consumer_and_token(self.linkedin.consumer, token=access_token, http_url=url)
        oauth_request.sign_request(self.linkedin.sig_method, self.linkedin.consumer, access_token)
        self._call_and_handle_low_level_error(lambda:self.linkedin.connection.request(oauth_request.http_method, url, headers=oauth_request.to_header()))
        xml = self.linkedin.connection.getresponse().read()
        dom = parseString(xml)
        errorDom = dom.getElementsByTagName('error')
        if len(errorDom) != 0  :
            raise LinkedInDomException(errorDom)
        return dom;

    def doApiPutRequest(self, url, body, access_token):
        """
        make a PUT call to linkedin and return the http status        
        """
        oauth_request = oauth.OAuthRequest.from_consumer_and_token(self.linkedin.consumer, token=access_token, http_method="PUT", http_url=url)
        oauth_request.sign_request(self.linkedin.sig_method, self.linkedin.consumer, access_token)
        self._call_and_handle_low_level_error(lambda:self.linkedin.connection.request(oauth_request.http_method, url, body=body, headers=oauth_request.to_header()))
        resp = self.linkedin.connection.getresponse()
        status = resp.status        
        resp.read() # this mandatory to keep the connection in a consistent state
        return status;
        
    def doApiPostRequest(self, url, body, access_token):
        """
        make a POST call to linkedin and return the http status        
        """
        oauth_request = oauth.OAuthRequest.from_consumer_and_token(self.linkedin.consumer, token=access_token, http_method="POST", http_url=url)
        oauth_request.sign_request(self.linkedin.sig_method, self.linkedin.consumer, access_token)
        self._call_and_handle_low_level_error(lambda:self.linkedin.connection.request(oauth_request.http_method, url, body=body, headers=oauth_request.to_header()))
        resp = self.linkedin.connection.getresponse()
        status = resp.status        
        resp.read() # this mandatory to keep the connection in a consistent state
        return status;
    
    def doApiDeleteRequest(self, url, access_token):
        """
        make a DELETE call to linkedin and return the http status        
        """
        oauth_request = oauth.OAuthRequest.from_consumer_and_token(self.linkedin.consumer, token=access_token, http_method="DELETE", http_url=url)
        oauth_request.sign_request(self.linkedin.sig_method, self.linkedin.consumer, access_token)
        self._call_and_handle_low_level_error(lambda:self.linkedin.connection.request(oauth_request.http_method, url, headers=oauth_request.to_header()))
        resp = self.linkedin.connection.getresponse()
        status = resp.status        
        resp.read() # this mandatory to keep the connection in a consistent state
        return status;


class LinkedInException(Exception):
        
    def __init__(self, mess):
        self.message = mess

    def __str__(self):
        return self.message

class LinkedInDomException(LinkedInException):
    '''
    Wrappe any error returned by a call to LinkedIn API
    '''
    errorDom = None

    def __init__(self,errorDom):
        self.errorDom = errorDom
        LinkedInException.__init__(self, self.getDomMessage())
        

    def __str__(self):
        return self.getDomMessage()

    def getDomMessage(self):
        '''
        return the original message from the xml dom
        '''
        return  self.errorDom[0].getElementsByTagName('message')[0].firstChild.nodeValue



class CommunicationApi(LinkedInApi):
    
    POST_MESSAGE_URL = LinkedIn.LI_API_URL + "/v1/people/~/mailbox"
    
    def __init(self, linkedin):
        LinkedInApi.__init__(self, linkedin)
    
    def sendMessage(self, recipients, subject, body, access_token):
        '''
        send a message to every person in recipients list
        - recipients : list of person ID
        - subject, message : no HTML 
        '''
        xmlPost = u"<?xml version='1.0' encoding='UTF-8'?>" \
                + "<mailbox-item>" \
                    + "<recipients>"
        for recipient in recipients:
            xmlPost = xmlPost + "<recipient> <person path='/people/" + recipient + "' />" \
                            + "</recipient>" 
        xmlPost = xmlPost + "</recipients>" \
                + "<subject>" + subject + "</subject>" \
                + "<body>" + body + "</body>" \
                + "</mailbox-item>"
        status = self.doApiPostRequest(self.POST_MESSAGE_URL, xmlPost, access_token)
        if status == 201:
            pass
        else:
            raise LinkedInException("LinkedIn response : " + str(status))
    
    def sendInvitation(self, id, subject, body, x_li_auth_token, access_token):
        '''
        send an invitation to join the user network
        The x_li_auth_token must be a string following the pattern name:value
        '''
        auth_token = x_li_auth_token.split(":")
        auth_token_name = auth_token[0]
        auth_token_value = auth_token[1]
        xmlPost = u"<?xml version='1.0' encoding='UTF-8'?>" \
                + "<mailbox-item>" \
                    + "<recipients>" \
                        + "<recipient>" \
                            + " <person path='/people/d=" + id + "' />" \
                        + "</recipient>" \
                    + "</recipients>" \
                    + "<subject>" + subject + "</subject>" \
                    + "<body>" + body + "</body>" \
                    + "<item-content>" \
                        + "<invitation-request>" \
                            + "<connect-type>friend</connect-type>" \
                            + "<authorization>" \
                                + "<name>" + auth_token_name + "</name>" \
                                + "<value>" + auth_token_value + "</value>" \
                            + "</authorization>" \
                        + "</invitation-request>" \
                    + "</item-content>" \
                + "</mailbox-item>"
        status = self.doApiPostRequest(self.POST_MESSAGE_URL, xmlPost, access_token)
        if status == 201:
            pass
        else:
            raise LinkedInException("LinkedIn response : " + str(status))
        
class ProfileApi(LinkedInApi):
    
    GET_SELF_PROFILE_URL = LinkedIn.LI_API_URL + "/v1/people/~"
    GET_CONNECTION_PROFILE_URL = LinkedIn.LI_API_URL + "/v1/people/id="

    SHORT_PROFILE_ATTRIBUTES = ":(id,first-name,last-name,headline,picture-url)"
    FULL_PROFILE_ATTRIBUTES = ":(id,first-name,last-name,headline,picture-url,location,industry,summary,positions)"
    API_STANDARD_PROFILE_ATTRIBUTES = ":(api-standard-profile-request)"
    
    def __init(self, linkedin):
        LinkedInApi.__init__(self, linkedin)
    
    def getMyShortProfile(self, access_token):
        '''
        return the xml DOM for the person. The xml contains the profil.
        '''
        dom = self.doApiRequest(self.GET_SELF_PROFILE_URL + self.SHORT_PROFILE_ATTRIBUTES, access_token)
        personDom  = dom.getElementsByTagName('person')[0]
        return personDom

    def getShortProfile(self, contactId, access_token):
        '''
        return the xml DOM for a given contact idenified by its id.
        The xml contains the profil.
        '''
        dom = self.doApiRequest(self.GET_CONNECTION_PROFILE_URL + contactId                            
                                + self.SHORT_PROFILE_ATTRIBUTES, access_token)
        personDom  = dom.getElementsByTagName('person')[0]
        return personDom
        
    def getMyFullProfile(self, access_token):
        '''
        return the xml DOM for the person. The xml contains the profil.
        '''
        dom = self.doApiRequest(self.GET_SELF_PROFILE_URL + self.FULL_PROFILE_ATTRIBUTES, access_token)
        personDom  = dom.getElementsByTagName('person')[0]
        return personDom

    def getFullProfile(self, contactId, access_token):
        '''
        return the xml DOM for a given contact idenified by its id.
        The xml contains the profil.
        '''
        dom = self.doApiRequest(self.GET_CONNECTION_PROFILE_URL + contactId
                                + self.FULL_PROFILE_ATTRIBUTES, access_token)
        personDom  = dom.getElementsByTagName('person')[0]
        return personDom
    
    def getApiStandardProfile(self, contactId, access_token):
        '''
        return the dom containing the url for API standard profile
        '''
        dom = self.doApiRequest(self.GET_CONNECTION_PROFILE_URL + contactId
                                + self.API_STANDARD_PROFILE_ATTRIBUTES, access_token)
        api_std_profile  = dom.getElementsByTagName('api-standard-profile-request')[0]
        return api_std_profile
        
        

class StatusApi(LinkedInApi):
    
    GET_STATUS_SELF_URL = LinkedIn.LI_API_URL + "/v1/people/~:(current-status)"
    SET_STATUS_SELF_URL = LinkedIn.LI_API_URL + "/v1/people/~/current-status"
    
    def __init__(self, linkedin):
        LinkedInApi.__init__(self, linkedin)
        
    def getMyStatus(self, access_token):
        '''
        return the status as a string
        '''
        dom  = self.doApiRequest(self.GET_STATUS_SELF_URL, access_token)
        peopleDom = dom.getElementsByTagName('person')
        myself = peopleDom[0]
        statusDom = myself.getElementsByTagName('current-status')
        if len(statusDom) == 0:
            mystatus = None
        else:
            mystatus = statusDom[0].firstChild.nodeValue
        return mystatus;
    
    def setMyStatus(self, status, access_token):
        # construct the xml body request
        xmlStatus = '<?xml version="1.0" encoding="UTF-8"?>' + "<current-status>" + status + "</current-status>"
        status  = self.doApiPutRequest(self.SET_STATUS_SELF_URL, xmlStatus, access_token)
        if status != 204:
            raise LinkedInException("LinkedIn response : " + str(status))
    
    def clearMyStatus(self, access_token):
        '''
        clear the status of the user definied by the access_token
        '''
        status   = self.doApiDeleteRequest(self.SET_STATUS_SELF_URL, access_token)       
        if status != 204:
            raise LinkedInException("LinkedIn response : " + str(status))

class ConnectionsApi(LinkedInApi):
    """
    How to get all of a user's connections:

        Note: This should happen after the linkedin redirect.  verifier is passed
        by LinkedIn back to your redirect page

        li = LinkedIn(LINKEDIN_API_KEY, LINKEDIN_SECRET_KEY)

        tokenObj = oauth.OAuthToken(requestTokenKey, requestTokenSecret)
        access_token = li.getAccessToken(tokenObj, verifier)

        connections = li.connections_api.getMyConnections(access_token)

        for c in connections:
            # Access c.firstname, c.lastname, etc.
    """

    CONNECTIONS_SELF = LinkedIn.LI_API_URL + "/v1/people/~/connections"
   
    def __init__(self, linkedin):
        LinkedInApi.__init__(self, linkedin)
    def getMyConnections(self, access_token):
        dom = self.doApiRequest(self.CONNECTIONS_SELF, access_token)

        peopleDom = dom.getElementsByTagName('person')

        return peopleDom

class NetworkApi(LinkedInApi):

    NETWORK_UPDATE = LinkedIn.LI_API_URL + "/v1/people/~/network"
    POST_NEWS_URL = LinkedIn.LI_API_URL + "/v1/people/~/person-activites"
    
    def __init__(self, linkedin):
        LinkedInApi.__init__(self, linkedin)

    def getNetworkUpdate(self, access_token):
        '''
        Retrieve all network update
        '''
        dom = self.doApiRequest(self.NETWORK_UPDATE, access_token)
        updateDom = dom.getElementsByTagName('update')

        return updateDom
    
    def sendNewsMessage(self, body, access_token):
        '''
        send a message to every contact in the network
        '''
        xmlPost = u"<?xml version='1.0' encoding='UTF-8'?>" \
                + "<activity locale=\"en_US\">" \
                    + "<content-type>linkedin-html</content-type>" \
                    + "<body>" + body + "</body>" \
                + "</activity>"
        status = self.doApiPostRequest(self.POST_NEWS_URL, xmlPost, access_token)
        if status == 201:
            pass
        else:
            raise LinkedInException("LinkedIn response : " + str(status))
