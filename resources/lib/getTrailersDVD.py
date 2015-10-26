# -*- coding: utf-8 -*-

import urllib
import urllib2
import re
import sys
import xbmcplugin
import xbmcgui

class main:
    def parse(self, selfGet):
        
        # vars
        self = selfGet
        
        mc = [
            ['Nadchodzące', 'week'],
            ['Styczeń', '0'],
            ['Luty', '1'],
            ['Marzec', '2'],
            ['Kwiecień', '3'],
            ['Maj', '4'],
            ['Czerwiec', '5'],
            ['Lipiec', '6'],
            ['Sierpień', '7'],
            ['Wrzesień', '8'],
            ['Październik', '9'],
            ['Listopad', '10'],
            ['Grudzień', '11']
            ]
            
        if 'arg' not in self.opt.keys():

            for key in mc:
                listItem = xbmcgui.ListItem(label=key[0])
                xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=sys.argv[0] + '?site=' + self.opt['site'] + '&arg=' + key[1], listitem=listItem, isFolder=True)
            
            xbmcplugin.endOfDirectory(int(sys.argv[1]))
        
        else:
        
            # połączenie z adresem URL, pobranie zawartości strony
            opener = urllib2.build_opener()
            
            if self.opt['arg'] == 'week':
                page = opener.open(self.URL + '/dvd/premieres').read()
            else:
                page = opener.open(self.URL + '/dvd/premieres?month=' + self.opt['arg'] + '&year=' + self.year).read()
                        
            # pobranie ID
            matchesID = list(set(re.compile('1\.fwcdn\.pl/po/[0-9]+/[0-9]+/([0-9]+)/[0-9]+\.').findall(page)))
                    
            # pobieranie trailerów
            if len(matchesID) != 0:
                import getTrailers
                getTrailers.main().parseTrailer(self, matchesID)
                