# -*- encoding: UTF-8 -*-

'''
Created on 9 mars 2010

@author: thierry
'''

import sys
import webbrowser

from zourite.core import zourite,plugin
from zourite.plugin.linkedin import linkedinplugin
from zourite.plugin.gmail import gmailplugin


from zourite.common import version


version.getInstance().submitRevision("$Revision: 159 $")


class AllPluginBootstrap():
    PLUGIN_LIST = [linkedinplugin.LinkedInPlugin(), gmailplugin.GmailPlugin()]
    
    def boot(self):
        zourite.ZOURITE_AVAILABLE_PLUGIN = self.PLUGIN_LIST



def runGui(argline=[]):
    
    from zourite.gui.zouriteGui import ZouriteGui 
    
    app = None
    if len(argline) > 1:
        if argline[1] == "mock":
            app = ZouriteGui(True)
        else:
            logging.warning("unknown argument " + argline[1] + ", ignored")
            bootstrap.AllPluginBootstrap().boot()
            app = ZouriteGui(False)
    else:   
        AllPluginBootstrap().boot()             
        app = ZouriteGui()
    # the hui is up and visible, so let's play
    app.run()


def configure(zcore, aPlugin):
    data = aPlugin.configure()
    while len(data) > 0:
    # print current value
        keys = data.keys()
        if plugin.PLUGIN_CONF_INFO in keys:
            print data[plugin.PLUGIN_CONF_INFO]
        
        if plugin.PLUGIN_CONF_WEBBROWSER in keys:
            url = data[plugin.PLUGIN_CONF_WEBBROWSER]
            print "please visit " + url
            webbrowser.open_new_tab(url)
        
        for key in keys:
        # handle special parameter
            if not key.startswith("__"):
                # standar parameter
                if data[key] is not None:
                    print "config param " + str(data[key])
                else:
                    input = raw_input("Please enter " + key + " :")
                    data[key] = input
        data = aPlugin.configure(data)
    print "configuration finished"
    print ""
    zcore.register_plugin(aPlugin)

    

    
def runSetup(force=False):
    '''
    This method should be run only if no plugin have been registered yet.
    This method try to load each plugin and mark them as registered e.g.
    to be load when zourite is instanciated.
    '''
    print "Zourite " + version.getInstance().getVersion()
    print "--------------------"
    print "Interactive Plugin Configuration Boostrap"
    print ""
    
    AllPluginBootstrap().boot() # inject all available plugin
    zcore = zourite.Zourite(auto_load=False) # create an instance of the core
    zcore.applyDefaultSettings()    
    for aPlugin in zourite.ZOURITE_AVAILABLE_PLUGIN: # for each available plugin
        print ">>>",aPlugin.get_plugin_id(),"<<<"    
        try:
            zcore.register_plugin(aPlugin) # register the plugin           
            if force:
                print "plugin configured, forced configuration..."
                configure(zcore, aPlugin)
            else:
                print "already configured !"
                print ""
        except plugin.ConfigurationRequiredExeption:
            print "not configured, starting configuration..."            
            configure(zcore, aPlugin)

    print "saving configuration..."
    zcore.save_registered_plugin() # save the current configuration of registered plugins
    print "configuration successful !!!"
        
if __name__ == "__main__":
        
    
    
    # check arg line if mock mode is required    
    argline = sys.argv
    if len(argline) > 1 and argline[1] == "setup":
        runSetup()
    elif len(argline) > 2 and argline[1] == "setup" and argline[2] == "force":
        runSetup(force=True)
    else:
        runGui(argline)

    