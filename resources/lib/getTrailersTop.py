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
            ['Top Nowości', '/rankings/film/premiere/world'],
            ['Top Świat', '/rankings/film/world'],
            ['Top Polska', '/rankings/film/poland'],
            ['Najbardziej oczekiwane: Nadchodzące premiery w Polsce', '/base/top/wantToSee/next30daysPoland'],
            ['Najbardziej oczekiwane: Nadchodzące premiery na świecie', '/base/top/wantToSee/next12monthsWorld'],
            ['Najbardziej chcecie obejrzeć: Premiery w Polsce', '/base/top/wantToSee/last30daysPoland'],
            ['Najbardziej chcecie obejrzeć: Premiery na świecie', '/base/top/wantToSee/last12monthsWorld'],
            ['Najbardziej chcecie obejrzeć: Filmy ostatnie dekady', '/base/top/wantToSee/lastDecadeFilms'],
            ['Najbardziej chcecie obejrzeć: Klasyki', '/base/top/wantToSee/classicalFilms']
            ]
            
        if 'arg' not in self.opt.keys():
        
            i = 0
            for key in mc:
                listItem = xbmcgui.ListItem(label=key[0])
                xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=sys.argv[0] + '?site=' + self.opt['site'] + '&arg=' + str(i), listitem=listItem, isFolder=True)
                i = i + 1
            xbmcplugin.endOfDirectory(int(sys.argv[1]))
        
        else:
        
            # połączenie z adresem URL, pobranie zawartości strony
            opener = urllib2.build_opener()
            page = opener.open(self.URL + mc[int(self.opt['arg'])][1]).read()
            
            # pobranie ID
            matchesID = list(set(re.compile('1\.fwcdn\.pl/po/[0-9]+/[0-9]+/([0-9]+)/[0-9]+\.').findall(page)))
                    
            # pobieranie trailerów
            if len(matchesID) != 0:
                import getTrailers
                getTrailers.main().parseTrailer(self, matchesID)
        