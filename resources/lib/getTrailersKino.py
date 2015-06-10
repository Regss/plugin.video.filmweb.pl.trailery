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
        
        mc = [
            ['Nadchodzące', 'week'],
            ['Styczeń', '1'],
            ['Luty', '2'],
            ['Marzec', '3'],
            ['Kwiecień', '4'],
            ['Maj', '5'],
            ['Czerwiec', '6'],
            ['Lipiec', '7'],
            ['Sierpień', '8'],
            ['Wrzesień', '9'],
            ['Październik', '10'],
            ['Listopad', '11'],
            ['Grudzień', '12']
            ]
            
        if self.opt2 == '':

            for key in mc:
                listItem = xbmcgui.ListItem(label=key[0])
                xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=sys.argv[0] + '?kino_' + key[1], listitem=listItem, isFolder=True)
            
            xbmcplugin.endOfDirectory(int(sys.argv[1]))
            
        else:

            # połączenie z adresem URL, pobranie zawartości strony
            opener = urllib2.build_opener()
            
            if self.opt2 == 'week':
                page = opener.open(self.URL + '/premiere').read()
            else:
                page = opener.open(self.URL + '/premiere/' + self.year + '/' + self.opt2).read()

            # pobieranie linków
            matchesLinkMovie = list(set(re.compile('entityTitle"><a href="([^"]+)"').findall(page)))
            
            # ograniczenie listy
            matchesLinkMovie = matchesLinkMovie[:self.settingsLimit]
        
            # jeśli istnieje trailer pobiera informacje
            if len(matchesLinkMovie) != 0:
                import parseTrailerPage
                parseTrailerPage.main().parseTrailer(self, matchesLinkMovie)
                