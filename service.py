# -*- coding: utf-8 -*-

import xbmc
import xbmcaddon

__addon__               = xbmcaddon.Addon()
__addon_id__            = __addon__.getAddonInfo('id')
__addonname__           = __addon__.getAddonInfo('name')
__icon__                = __addon__.getAddonInfo('icon')
__addonpath__           = xbmc.translatePath(__addon__.getAddonInfo('path')).decode('utf-8')

class Monitor(xbmc.Monitor):

    def __init__(self):
        xbmc.Monitor.__init__(self)
        
    def onScreensaverActivated(self):
        xbmc.executebuiltin('XBMC.RunPlugin(plugin://' + __addon_id__ + '/?service=1)')

class Player(xbmc.Player):
    def __init__(self):
        xbmc.Player.__init__(self)
        
    def onPlayBackStopped(self):
        xbmc.executebuiltin('XBMC.RunPlugin(plugin://' + __addon_id__ + '/?service=2)')
            
monitor = Monitor()
player = Player()

while(not xbmc.abortRequested):
    xbmc.sleep(100)
    