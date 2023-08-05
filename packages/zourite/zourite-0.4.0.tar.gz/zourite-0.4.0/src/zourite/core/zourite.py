# -*- encoding: UTF-8 -*-

import plugin
import logging
import pickle
import os
import os.path

import dbus

from ..common import version # must be relative cause in the current package there is a module named zourite yet


version.getInstance().submitRevision("$Revision: 288 $")

ZOURITE_AVAILABLE_PLUGIN = None

NOT_YET_IMPLEMENTED = 'not yet implemented'

MEMORY_CACHE_STORE = "MEMORY_CACHE_STORE"
DISK_CACHE_STORE = "DISK_CACHE_STORE"

AVAILABLE_CACHE_STORE= [MEMORY_CACHE_STORE, DISK_CACHE_STORE]

def get_zourite_storage_dir(self):
    '''
    Compute the application storage dir.
    This is an utility function to retrieve the directory where zourite can
    store any file like settings or cached data.
    '''
    storage = os.path.expanduser("~")
    storage = os.path.join(storage, ".zourite")
    return storage

class Zourite(plugin.ZouritePlugin):
    '''
    The main class of the application (except the GUI). Zourite is a professional network
    application. The core concept is in plugin module and Zourite itself is a plugin which
    is intended for aggregate all other plugin. Currently there is only one plugin in other
    word one supported network: LinkedIn.
    '''
    registered_plugin = []
       
    settings = None
    
    
    def __init__(self, auto_load=True):
        # read registered plugin
        if auto_load:
            self.load_settings()
            self.apply_settings()
        
    
    def load_settings(self):
        '''
        load the saved settings
        '''
        self.ensure_zourite_conf_store()
        storage = self.get_zourite_settings_file()
        try:           
            file = open(storage,'rb')
            self.settings = pickle.load(file)
            file.close()
        except IOError, EOFError:
            logging.warning("failed to load the settings")
            self.settings  = Settings()
            
    
    def save_settings(self):
        '''
        save the current settings
        '''
        self.ensure_zourite_conf_store()
        storage = self.get_zourite_settings_file()
        try:           
            file = open(storage,'wb')
            pickle.dump(self.settings,file)
            file.close()
        except IOError:
            logging.warning("failed to save the settings")

    
    def apply_settings(self):
        self.load_registered_plugin()
   

    def get_zourite_settings_file(self):
        storage = get_zourite_storage_dir(self)
        storage = os.path.join(storage, "settings.pickle")
        return storage

   
    def load_registered_plugin(self):
        '''
        read the settings and load registered plugin
        '''        
        for pluginid in self.settings.registered_plugin_ids:
            
            plugin = self.get_available_plugin_by_id(pluginid)
            # which cache storage we will used ?
            if self.settings.cache_storage == MEMORY_CACHE_STORE:
                cachePlugin = MemoryCachePlugin(plugin)
            elif self.settings.cache_storage == DISK_CACHE_STORE:
                cachePlugin = DiskCachePlugin(plugin)
            else:
                cachePlugin = MemoryCachePlugin(plugin)
                logging.warning("the current cache store " + str(self.settings.cache_storage) + " is unknown")
                logging.warning("will use " + MEMORY_CACHE_STORE + " for " + plugin.get_plugin_id())
                
            if  self.settings.cache_strategy == CachePlugin.CACHE_PREFERED_STATEGY:
                cachePlugin.setCachePrefered()
            elif self.settings.cache_strategy == CachePlugin.NETWORK_DATA_PREFERED_STRATEGY:
                cachePlugin.setNetworkPrefered()
            else:
                logging.warning("the current cache strategy " + str(self.settings.cache_strategy) + " is unknow")
                logging.warning("will use " + cachePlugin.cacheStrategy + " for " + cachePlugin.get_plugin_id())
            
            self.register_plugin(cachePlugin)
       
    

        
      
    def save_registered_plugin(self):
        '''
        save current registered plugin in the settiongs then save the settings
        '''
        self.settings.registered_plugin_ids[:]
        for plugin in self.registered_plugin:
            self.settings.registered_plugin_ids.append(plugin.get_plugin_id())
        self.save_settings()

    def unregister_all_plugin(self):
        '''
        remove all registered plugin. This means all plugin are removed from memory
        but the settings is not modified.
        '''
        del self.registered_plugin[:]
        
    def register_plugin(self, plugin):
        '''
        Launch the plugin and remember it as registered.
        '''
        # this is a bare implementation 
        plugin.run_plugin()
        self.registered_plugin.append(plugin)
        
        
   
    def ensure_zourite_conf_store(self):
        storage = get_zourite_storage_dir(self)
        if os.path.exists(storage):
            pass
        else:
            os.makedirs(storage)
    
    
    def get_available_plugin_by_id(self, pluginid):
        for p in ZOURITE_AVAILABLE_PLUGIN:
            if p.get_plugin_id() == pluginid:
                return p
        mess = "the plugin for id " + str(pluginid) + " not found"
        raise RuntimeError(mess)
    
    def get_plugin_by_id(self, networkid):
        '''
        Look inside registered plugin list e.g. loaded plugin
        and return the which one with the given id
        '''
        for p in self.registered_plugin:
            if p.get_plugin_id() == networkid:
                return p
        mess = "the plugin for id " + str(networkid) + " not found"
        raise RuntimeError(mess)
    
    
    
    def get_short_profile(self, id, networkid):
        plugin = self.get_plugin_by_id(networkid)
        return plugin.getShortProfile(id)
    
    
    
    '''
    Facade 
    '''
    
    def isNewsAutoRefreh(self):
        return self.settings.news_auto_refresh
    
    def isMergeContact(self):
        return self.settings.merge_contact
    
    def resetCacheData(self):
        for plugin in self.registered_plugin:
            plugin.resetCacheData()
    
    def setForceRefresh(self, enabled):
       for plugin in self.registered_plugin:
           plugin.setBypassCache(enabled)
    
    def applyAndSaveSettings(self, new_settings):
        '''
        apply the new settings in arguments and save it
        '''
        self.unregister_all_plugin()
        self.settings = new_settings
        self.apply_settings()
        self.save_settings()
        
    def applyDefaultSettings(self):
        self.applyAndSaveSettings(Settings())
    
    def getRegisteredPlugin(self):
        return self.registered_plugin
    
    def getCurrentCacheStrategy(self):
        return self.settings.cache_strategy
    
    def getCurrentCacheStorage(self):
        return self.settings.cache_storage
    
    def getAvailableCacheStore(self):
        '''
        The availbale cache store.
        Each one can be uesed to modify the place zourite will cache data.
        For instance cache data may be stored in memory for efficience or
        on disk for persistence.
        '''
        return AVAILABLE_CACHE_STORE
    
    def getAvailableCacheStrategies(self):
        '''
        The available cache strategy. 
        Each one can be used to modify the way zourite use the cache.
        For instance it can prefer fresh data from the network and use information
        from cache only when the network can't be reached.
        '''
        return CachePlugin.AVAILABLE_CACHE_STRATEGIES
    
    def getAvailablePlugins(self):
        '''
        The available plugin.
        Each one can be activated and used by zourite as network to fetch information
        from. 
        '''
        return ZOURITE_AVAILABLE_PLUGIN
    
    def getPluginAmongAvailable(self,plugin_id):
        '''
        Search for a plugin among all available plugin.
        '''    
        availablePLugins = self.getAvailablePlugins()
        result = filter(lambda(x): x.get_plugin_id() == plugin_id, availablePLugins)
        plug = None
        if len(result) >  0:
            plug =  result[0]
        return plug
            
    
    def getShortProfileForNetUpdateStatus(self, netUpdateConn):
        '''
        Facade method to retrieve a short profile for a given status update event
        '''
        id = netUpdateConn.connection.id
        networkid = netUpdateConn.networkId
        return self.get_short_profile(id, networkid)
        
        
    def getShortProfileForNetUpdateJoinGroup(self, netUpdateConn):
        '''
        Facade method to retrieve a short profile for a given join group event
        '''
        id = netUpdateConn.connection.id
        networkid = netUpdateConn.networkId
        return self.get_short_profile(id, networkid)

        
    def getShortProfileForNetUpdateProfile(self, netUpdateConn):
        '''
        Facade method to retrieve the short profile for the contact that
        have updated his/her profile        
        '''
        id = netUpdateConn.connection.id
        networkid = netUpdateConn.networkId
        return self.get_short_profile(id, networkid)
        
    
    def getShortProfilesForNetUpdateConnection(self, netUpdateConn):
        '''
        given a network update connection, return a tuple containin short profile
        for the existing connection and the new connection
        '''
        myconn = self.get_short_profile(netUpdateConn.connection.id, netUpdateConn.networkId)
        newconn = self.get_short_profile(netUpdateConn.newConnection.id, netUpdateConn.networkId)
        return myconn, newconn
    
    def getShortProfileForNetUpdateSelfConnection(self, netUpdateSelfConn):
        '''
        Given a netwokr update self connection, return the short profile for the new connection
        '''
        id = netUpdateSelfConn.newConnection.id
        networkid = netUpdateSelfConn.networkId
        return self.get_short_profile(id, networkid)
    
    
    def isConnectedTo(self, shortProfile):
        '''
        Test is the given short profile is a connection
        '''
        plugin = self.get_plugin_by_id(shortProfile.networkId)
        myConnections = plugin.getMyConnections()
        result = filter(lambda(p): p.id == shortProfile.id, myConnections)
        return  len(result) > 0
    
    def getGtkImageForProfile(self, shortProfile):
        '''
        return a gtk.Image for the profile
        '''
        plugin = self.get_plugin_by_id(shortProfile.networkId)
        return plugin.getGtkImage(shortProfile)
    
    def getGtkPixBufForProfile(self, shortProfile):
        '''
        return a gtk.Image for the profile
        '''
        plugin = self.get_plugin_by_id(shortProfile.getNetworkId())
        return plugin.getGdkPixbuf(shortProfile)
    
    def getGtkPixBufForNetwork(self, networkId):
        '''
        return a pixbuf as picture for the network plugin
        '''
        plugin = self.get_plugin_by_id(networkId)
        return plugin.getPluginLogoPixbuf()
    
    def getGtkPixBufForPerson(self, person):
        '''
        return a pixbuf as picture for the network plugin
        '''    
        sp = self.get_short_profile(person.id, person.networkId)
        plugin = self.get_plugin_by_id(person.networkId)
        return plugin.getGdkPixbuf(sp)
    
    
    def getFullProfileForMergedShortProfile(self, mergedShortProfile):
        '''
        Try to find a full profile from any underlying short profile
        '''
        if (mergedShortProfile.networkId is  None or len(mergedShortProfile.networkId) == 0) \
            or (mergedShortProfile.id is None or len(mergedShortProfile.id) == 0) :
            # defined the preferred network
            for sp in mergedShortProfile.underlying_sp:
                mergedShortProfile.networkId = sp.networkId
                mergedShortProfile.id = sp.id
                try:
                   fp = self.getFullProfileForShortProfile(sp)
                except plugin.UnvailableException:
                    pass
                else:
                    # a caching facility
                    mergedShortProfile.networkId = sp.networkId
                    mergedShortProfile.id = sp.id
                    return fp
                
        return self.getFullProfileForShortProfile(mergedShortProfile)
        
      
    def getFullProfileForShortProfile(self, shortProfile):
        networkId = shortProfile.networkId
        contactId = shortProfile.id
        return self.get_plugin_by_id(networkId).getFullProfile(contactId) 
    
    def getFullProfileForShortPerson(self, person):
        networkId = person.networkId
        contactId = person.id
        return self.get_plugin_by_id(networkId).getFullProfile(contactId) 
    
    
    def sendConnectionRequestToProfile(self, shortProfile, subject, body):
        '''
        Send an invitation request to a given profile. Subject and body of the
        message must be provided
        '''
        plugin = self.get_plugin_by_id(shortProfile.networkId)
        plugin.sendInvitationRequest(shortProfile.id, subject, body)
    
    def sendMessageToProfile(self, shortProfile, subject, body):
        '''
        Send a message to a connected person.
        '''
        plugin = self.get_plugin_by_id(shortProfile.networkId)
        plugin.sendMessageRequest(shortProfile.id, subject, body)
    
    def getAllMyStatus(self):
        '''
        Return a set of all status grabbed from every network plugin.
        '''
        status = []
        for aPlugin in self.registered_plugin:
            aStatus = aPlugin.getMyStatus()
            if aStatus == None:
                pass
            elif len(aStatus) > 0:
                status.append(aStatus)
        return set(status)
        
    '''
    Interface for any network that can be used by zourite
    '''
    
    
    
    def getMyConnections(self):
        connections = []
        for aPlugin in self.registered_plugin:
            shortProfileForAPlugin = aPlugin.getMyConnections()
            if self.settings.merge_contact:
                for sp in shortProfileForAPlugin:
                    # find existing contact to merge with
                    matching_sp_lst = filter(lambda(x): x.isSamePerson(sp), connections)
                    if len(matching_sp_lst) == 0:
                        merged_sp = MergedShortProfile()
                        merged_sp.addShortProfile(sp)
                        connections.append(merged_sp)
                    else:
                        matching_sp = matching_sp_lst[0]
                        # merge sp into matching_sp
                        matching_sp.addShortProfile(sp)                                        
            else :
                connections.extend(shortProfileForAPlugin)                
        return connections
    
    def setMyStatus(self, status):
        for aPlugin in self.registered_plugin:
            aPlugin.setMyStatus(status)
        
        # TODO : issue 17    
        # dbus-send --type=method_call --print-reply --dest=org.freedesktop.Telepathy.MissionControl /org/freedesktop/Telepathy/MissionControl org.freedesktop.Telepathy.MissionControl.SetPresence uint32:2 string:"I'm here"
        
    
    def clearMyStatus(self):
        for aPlugin in self.registered_plugin:
            aPlugin.clearMyStatus()
    

    def getNetworkUpdate(self):
        news = []
        for aPlugin in self.registered_plugin:
            news.extend(aPlugin.getNetworkUpdate())
        return news
    
    def sendMessageToNetwork(self, body):
        for aPlugin in self.registered_plugin:
            aPlugin.sendMessageToNetwork(body)


class MergedShortProfile(plugin.ShortProfile):
    '''
    an implementation of ShortProfile that merge information about a person coming from multiple
    network
    '''    

    def __init__(self):
       self.underlying_sp = [] 
    
    def addShortProfile(self, sp):
        self.underlying_sp.append(sp)
    
    def _is_not_null(self, value):
        if value is None:
            return False
        elif isinstance(value, str):
            return len(value) > 0
        else:
            return True
        
    def _retrieve_attribute(self, getter, not_found_value = ""):
        filtered = filter(lambda(x): self._is_not_null(getter(x)), self.underlying_sp)
        if len(filtered) > 0:
            # take the first non null value
            # TODO : this should be a user defined choice
            return getter(filtered[0])
        else:
            return not_found_value

    def getFirstname(self):
        return self._retrieve_attribute(lambda(x):x.getFirstname())

    def getLastname(self):
        return self._retrieve_attribute(lambda(x):x.getLastname())


    def getPhone(self):
        # return phone number found in one of the merged profil
        return self._retrieve_attribute(lambda(x):x.getPhone(), None)
        

    def getEmail(self):
        return self._retrieve_attribute(lambda(x):x.getEmail(), None)
        

    def getPicture(self):
        return self._retrieve_attribute(lambda(x):x.getPicture(), None)

    def getHeadline(self):
        return self._retrieve_attribute(lambda(x):x.getHeadline())

    def getNetworkId(self):
        return self._retrieve_attribute(lambda(x):x.getNetworkId())

            
        


class Settings():
    '''
    Represents the settings for Zourite
    '''
   
    def __init__(self):
        self.registered_plugin_ids = []
        self.cache_strategy = CachePlugin.NETWORK_DATA_PREFERED_STRATEGY    
        self.cache_storage = MEMORY_CACHE_STORE
        self.news_auto_refresh = False
        self.merge_contact = False
    

class CacheStore():
    '''
    Represent the underlying storage for a cache.
    '''
    
    def getData(self, key):
        '''
        Retrieve the data stored under the given key
        '''
        raise RuntimeError(NOT_YET_IMPLEMENTED)
    
    def setData(self, key, value):
        '''
        Store the given data under the given key.
        '''
        raise RuntimeError(NOT_YET_IMPLEMENTED)
    
    def removeKey(self, key):
        '''
        remove the data stored under the given key
        '''
        raise RuntimeError(NOT_YET_IMPLEMENTED)
    
    def containsKey(self, key):
        '''
        Test if this cache contains data for the given key
        '''
        raise RuntimeError(NOT_YET_IMPLEMENTED)
    
    def clear(self):
        '''
        Clear all data in this cache
        '''
        raise RuntimeError(NOT_YET_IMPLEMENTED)
     
class MemoryStore(CacheStore):
    '''
    In memory store for caching feature
    '''

    dataStore = None

    def __init__(self):
        self.dataStore = {}

    def clear(self):
        self.dataStore.clear()

    def removeKey(self, key):
        del self.dataStore[key]
        
    def getData(self, key):
        return self.dataStore[key]

    def setData(self, key, value):
        self.dataStore[key] = value

    def containsKey(self, key):
        return key in self.dataStore
        

class DiskStore(CacheStore):
    '''
    On disk (persistent) store for caching feature.    
    '''
    dataStore = None # path where data will be stored
    entity  = None
    
    def __init__(self, pluginid,  entity):
        self.entity = entity
        self.pluginid = pluginid        
        self._init_cache_dir()
    
    def __str__(self):
        return "Disk store for entity [" + self.entity + "]"
    
    def _init_cache_dir(self):
        self.dataStore = get_zourite_storage_dir(self)
        self.dataStore = os.path.join(self.dataStore,"cache")
        self.dataStore = os.path.join(self.dataStore,self.pluginid)
        self.dataStore = os.path.join(self.dataStore,self.entity)
        if os.path.exists(self.dataStore):
            pass
        else:
            os.makedirs(self.dataStore)
    
    def _get_storage_for_key(self, key):
        key_storage = os.path.join(self.dataStore, str(key))
        return key_storage

        
    def clear(self):
        for file in os.listdir(self.dataStore):
            filepath = os.path.join(self.dataStore, file)
            os.remove(filepath)
        os.removedirs(self.dataStore)
        self._init_cache_dir()

    def removeKey(self, key):
        key_storage = self._get_storage_for_key(key)
        os.remove(key_storage)
        
    def getData(self, key):
        key_storage = self._get_storage_for_key(key)
        try:
            file = open(key_storage,'rb')
            data = pickle.load(file)
            file.close()
            
        except IOError:
            logging.error("failed to read data " + str(key) + " from cache " + self.__str__())           
            raise
        
        return data

    def setData(self, key, value):
        key_storage = self._get_storage_for_key(key)
        try:
            file = open(key_storage,'wb')
            pickle.dump(value, file)
            file.close()
            
        except IOError:
            logging.warn("failed to write data " + str(key) + " into cache " + self.__str__())
                

    def containsKey(self, key):
        key_storage = self._get_storage_for_key(key)
        return os.path.exists(key_storage)


class CachePlugin(plugin.ZouritePlugin):
    '''
    This class is used by zourite to enable caching on regular plugin.
    The main goal is to provide a not connected usability of Zourite by
    using data previously loaded by the cache.
    '''
    
    shortProfileCache = None
    fullProfileCache = None
    connectionCache = None
    networkUpdateCache = None
    
    DUMMY_KEY = 1   # used for a call that don't have a key
    
    CACHE_PREFERED_STATEGY = "CACHE_PREFERED_STATEGY"
    NETWORK_DATA_PREFERED_STRATEGY = "NETWORK_DATA_PREFERED_STRATEGY"    
        
    AVAILABLE_CACHE_STRATEGIES = [CACHE_PREFERED_STATEGY, NETWORK_DATA_PREFERED_STRATEGY]
    
    cacheStrategy = None
    
    forceRefresh = False # bypass the strategy and force call to the legacy plugin
    

    def __init__(self, realPlugin):
        self.pluginImpl = realPlugin
        self.setNetworkPrefered()
        self._forceRefresh = False
    
    def _getMethod(self, fonction, key, cache):
        '''
        Appelle la fonction en paramètre en prenant en compte le cache.        
        '''
        if self.cacheStrategy == self.CACHE_PREFERED_STATEGY and not self.forceRefresh :
            if cache.containsKey(key) :
                value = cache.getData(key)
            else:
                value = fonction()
                cache.setData(key,value)
            return value
        elif self.cacheStrategy == self.NETWORK_DATA_PREFERED_STRATEGY or self.forceRefresh:
            try:
                value = fonction()
                cache.setData(key,value)
            except plugin.UnvailableException:
                if cache.containsKey(key):
                    value = cache.getData(key)
                else:
                    raise
            return value
        else:
            return fonction()

    def setBypassCache(self, enable):
        self.forceRefresh = enable
        
    def resetCacheData(self):
        '''
        Delete data in cache
        '''
        self.connectionCache.clear()
        self.fullProfileCache.clear()
        self.networkUpdateCache.clear()
        self.shortProfileCache.clear()
        
        
    def setCachePrefered(self):
        self.cacheStrategy = self.CACHE_PREFERED_STATEGY
    
    def setNetworkPrefered(self):
        self.cacheStrategy = self.NETWORK_DATA_PREFERED_STRATEGY
        
    def run_plugin(self):
        self.pluginImpl.run_plugin()
    
    def get_plugin_id(self):
        return self.pluginImpl.get_plugin_id()
    
    def getMyConnections(self):
        # the key used have no importance because the current method have no parameter so no key is required for the cache       
        return self._getMethod(lambda: self.pluginImpl.getMyConnections(), self.DUMMY_KEY, self.connectionCache)
            
    def getMyStatus(self):
        return self.pluginImpl.getMyStatus()
        
    def setMyStatus(self, status):
        self.pluginImpl.setMyStatus(status)
          
    def clearMyStatus(self):
        self.pluginImpl.clearMyStatus()

    def getNetworkUpdate(self):
        return self._getMethod(lambda: self.pluginImpl.getNetworkUpdate(), self.DUMMY_KEY, self.networkUpdateCache)
        
    def getShortProfile(self,contactId):
        return self._getMethod(lambda: self.pluginImpl.getShortProfile(contactId), contactId, self.shortProfileCache)
    
    def getFullProfile(self, contactId):
        return self._getMethod(lambda: self.pluginImpl.getFullProfile(contactId), contactId, self.fullProfileCache)
    
    def getMyShortProfile(self):
        return self.pluginImpl.getMyShortProfile()
    
    def getMyFulllProfile(self):
        return self.pluginImpl.getMyFullProfile()
    
    def getGtkImage(self, shortProfile):
        return self.pluginImpl.getGtkImage(shortProfile)
    
    def getGdkPixbuf(self, shortProfile):
        return self.pluginImpl.getGdkPixbuf(shortProfile)
    
    
    def getPluginLogoPixbuf(self):
        return self.pluginImpl.getPluginLogoPixbuf()

    def sendInvitationRequest(self, contactId, subject, body):
        self.pluginImpl.sendInvitationRequest(contactId,subject,body)
    
    def sendMessageRequest(self, contactId, subject, body):
        self.pluginImpl.sendMessageRequest(contactId,subject, body)
        
    def sendMessageToNetwork(self, body):
        self.pluginImpl.sendMessageToNetwork(body)
        
        
class MemoryCachePlugin(CachePlugin):
    '''
    Cache plugin that store data in memory
    '''
    def __init__(self, realPlugin):
        CachePlugin.__init__(self, realPlugin)
        self.shortProfileCache = MemoryStore()
        self.fullProfileCache = MemoryStore()
        self.connectionCache = MemoryStore()
        self.networkUpdateCache = MemoryStore()
        
        
class DiskCachePlugin(CachePlugin):
    '''
    Cache plugin that store data on disk (e.g. in a persistent way)
    '''
    def __init__(self, realPlugin):
        CachePlugin.__init__(self, realPlugin)
        plugin_id = realPlugin.get_plugin_id()
        self.shortProfileCache = DiskStore(plugin_id,"short_profile")
        self.fullProfileCache = DiskStore(plugin_id,"full_profile")
        self.connectionCache= DiskStore(plugin_id,"connection")
        self.networkUpdateCache = DiskStore(plugin_id, "network_update")