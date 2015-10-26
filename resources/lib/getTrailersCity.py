# -*- coding: utf-8 -*-

import urllib
import urllib2
import re
import sys
import xbmcplugin
import xbmcgui

import getTrailers

class main:
    def parse(self, selfGet):
        
        # vars
        self = selfGet
        encodeCity = urllib.quote(self.settingsCity)
        
        if 'arg' not in self.opt.keys():

            opener = urllib2.build_opener()
            page = opener.open(self.URL + '/showtimes/' + encodeCity).read()
            
            matchListDays = re.search('day-switcher top-20"?>(.*?)</ul>', page)
            matchDays = re.compile('<a[^>]+>([^<]+)<br>([^<]+)</a>').findall(matchListDays.group(1))
            
            i = 0;
            for key in matchDays:
                listItemCity = xbmcgui.ListItem(label=key[0] + key[1])
                xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=sys.argv[0] + '?site=' + self.opt['site'] + '&arg=' + str(i), listitem=listItemCity, isFolder=True)
                i += 1;
                
            xbmcplugin.endOfDirectory(int(sys.argv[1]))
            
        else:
            
            # połączenie z adresem URL, pobranie zawartości strony
            opener = urllib2.build_opener()
            page = opener.open(self.URL + '/showtimes/' + encodeCity + '?day=' + self.opt['arg']).read()
            
            # pobranie ID
            matchesID = list(set(re.compile('film-([0-9]+)').findall(page)))
                    
            # pobieranie trailerów
            if len(matchesID) != 0:
                getTrailers.main().parseTrailer(self, matchesID)
