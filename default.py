# -*- coding: utf-8 -*-

import urllib
import urllib2
import os
import re
import sys
import xbmc
import xbmcaddon
import xbmcplugin
import xbmcgui
import datetime
import json

__addon__               = xbmcaddon.Addon()
__addonpath__           = xbmc.translatePath(__addon__.getAddonInfo('path'))
__path__                = os.path.join(__addonpath__, 'resources', 'lib' )
__path_img__            = os.path.join(__addonpath__, 'resources', 'media' )

sys.path.append (__path__)
sys.path.append (__path_img__)

import debug

class Trailers:
    def __init__(self):
        self.settingsAutoPlay               = __addon__.getSetting('autoPlay')
        self.settingsCity                   = __addon__.getSetting('city')
        self.settingsScreenSaverAutoPlay    = __addon__.getSetting('screenSaverAutoPlay')
        self.settingsScreenSaverSection     = __addon__.getSetting('screenSaverSection')
        self.settingsCheckNew               = __addon__.getSetting('checkNew')
        self.URL                            = 'http://www.filmweb.pl'
        self.MOVIES                         = []
        date                                = datetime.datetime.now()
        self.year                           = str(date.year)
        
        debug.debug(str(sys.argv))
        
        self.opt = {}
        # pobranie zmiennych
        optStr = sys.argv[2][1:]
        pair = optStr.split('&')
        for p in pair:
            nv = p.split('=')
            if len(nv) > 1:
                self.opt[nv[0]] = nv[1]
        
        self.start()
        
    def start(self):
        debug.debug('opt: ' + str(self.opt))
        
        # check new DVD premiere to wanna see and notify
        if 'true' in self.settingsCheckNew:
            if 'service' in self.opt.keys() and self.opt['service'] == '2':
                import getTrailersAfterPremiere as load
                ret = load.main().parse(self)
                if ret == False:
                    return False
                debug.notify(str(len(ret)) + ' Nowych premier DVD')
                return
        
        # if start from service set args
        if 'service' in self.opt.keys() and self.opt['service'] == '1':
            # check if player not playing
            jsonPlayer = '{"jsonrpc": "2.0", "method": "Player.GetActivePlayers", "id": "1"}'
            jsonGetPlayer = xbmc.executeJSONRPC(jsonPlayer)
            jsonGetPlayer = unicode(jsonGetPlayer, 'utf-8', errors='ignore')
            jsonGetPlayerResponse = json.loads(jsonGetPlayer)
            if 'result' in jsonGetPlayerResponse and len(jsonGetPlayerResponse['result']) == 0 and 'true' in self.settingsScreenSaverAutoPlay:
                s = [['kino', 'week'], ['dvd', 'week'], ['filmweb', self.year], ['wannasee', ''], ['city', ''], ['afterpremiere', '']]
                self.opt['site'] = s[int(self.settingsScreenSaverSection)][0]
                self.opt['arg'] = s[int(self.settingsScreenSaverSection)][1]
            else:
                return
    
        debug.debug('opt: ' + str(self.opt))
        
        if 'site' not in self.opt.keys():
            import menu as load
        elif self.opt['site'] == 'kino':
            import getTrailersKino as load
        elif self.opt['site'] == 'dvd':
            import getTrailersDVD as load
        elif self.opt['site'] == 'filmweb':
            import getTrailersFilmweb as load
        elif self.opt['site'] == 'top':
            import getTrailersTop as load
        elif self.opt['site'] == 'wannasee':
            import getTrailersSee as load
        elif self.opt['site'] == 'city':
            import getTrailersCity as load
        elif self.opt['site'] == 'friends':
            import getTrailersFriends as load
        elif self.opt['site'] == 'afterpremiere':
            import getTrailersAfterPremiere as load
        else:
            import menu as load
        
        if load.main().parse(self) == False:
            return False
        self.playList()
    
    # PLAYLIST
    def playList(self):
        xbmcplugin.setContent(int(sys.argv[1]),'movies')
        xbmcplugin.endOfDirectory(int(sys.argv[1]))
        
        # utworzenie Playlisty
        playList = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
        playList.clear()
        for playListItem in self.MOVIES:
            playList.add(playListItem['url'], playListItem['item'])
        
        # autoodtwarzanie playlisty
        if self.settingsAutoPlay == 'true':
            xbmc.Player().play(playList)
    
Trailers()
