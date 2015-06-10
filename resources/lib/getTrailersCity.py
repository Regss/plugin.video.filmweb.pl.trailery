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
        encodeCity = urllib.quote(self.settingsCity)
        
        if self.opt2 == '':

            opener = urllib2.build_opener()
            page = opener.open(self.URL + '/showtimes/' + encodeCity).read()
            
            matchListDays = re.search('day-switcher top-20"?>(.*?)</ul>', page)
            matchDays = re.compile('<a[^>]+>([^<]+)<br>([^<]+)</a>').findall(matchListDays.group(1))
            
            i = 0;
            for key in matchDays:
                listItemCity = xbmcgui.ListItem(label=key[0] + key[1])
                xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=sys.argv[0] + '?city_' + str(i), listitem=listItemCity, isFolder=True)
                i += 1;
                
            xbmcplugin.endOfDirectory(int(sys.argv[1]))
            
        else:
            
            # połączenie z adresem URL, pobranie zawartości strony
            opener = urllib2.build_opener()
            page = opener.open(self.URL + '/showtimes/' + encodeCity + '?day=' + self.opt2).read()
            
            # pobranie linków do poszczególnych filmów
            matchesLinkMovie = list(set(re.compile('<a class="name[^>]+href="(/film/[^/]+)/').findall(page)))
            
            # ograniczenie listy
            matchesLinkMovie = matchesLinkMovie[:self.settingsLimit]
        
            # jeśli istnieje trailer pobiera informacje
            if len(matchesLinkMovie) != 0:
                import parseTrailerPage
                parseTrailerPage.main().parseTrailer(self, matchesLinkMovie)
