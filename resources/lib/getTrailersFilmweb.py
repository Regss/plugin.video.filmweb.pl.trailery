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
import HTMLParser
import datetime

__addon__               = xbmcaddon.Addon()
__addon_id__            = __addon__.getAddonInfo('id')
__addonname__           = __addon__.getAddonInfo('name')
__icon__                = __addon__.getAddonInfo('icon')
__addonpath__           = xbmc.translatePath(__addon__.getAddonInfo('path'))
__lang__                = __addon__.getLocalizedString
__path__                = os.path.join(__addonpath__, 'resources', 'lib' )
__path_img__            = os.path.join(__addonpath__, 'resources', 'media' )

sys.path.append (__path__)
sys.path.append (__path_img__)

class main:
    def parse(self, selfGet):
        
        # vars
        self = selfGet
        
        if self.opt2 == '':
            
            opener = urllib2.build_opener()
            page = opener.open(self.URL + '/filmwebRecommends/').read()
            matchesYearsRecommended = list(set(re.compile('href="/filmwebRecommends/([0-9]+)"').findall(page)))
            matchesYearsRecommended.sort(reverse=True)
            
            listItem = xbmcgui.ListItem(label=self.year)
            xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=sys.argv[0] + '?filmweb_' + self.year, listitem=listItem, isFolder=True)    
            
            for key in matchesYearsRecommended:
                listItem = xbmcgui.ListItem(label=key)
                xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=sys.argv[0] + '?filmweb_' + key, listitem=listItem, isFolder=True)
            
            xbmcplugin.endOfDirectory(int(sys.argv[1]))
        
        else:
        
            # połączenie z adresem URL, pobranie zawartości strony
            opener = urllib2.build_opener()
            page = opener.open(self.URL + '/filmwebRecommends/' + self.opt2).read()
                        
            # pobranie linków do poszczególnych filmów
            matchesLinkMovie = list(set(re.compile('filmBox"><a href="([^"]+)"').findall(page)))
            
            # ograniczenie listy
            matchesLinkMovie = matchesLinkMovie[:self.settingsLimit]
        
            # jeśli istnieje trailer pobiera informacje
            if len(matchesLinkMovie) != 0:
                import parseTrailerPage
                parseTrailerPage.main().parseTrailer(self, matchesLinkMovie)
                    