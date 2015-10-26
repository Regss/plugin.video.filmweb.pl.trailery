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
        
        if 'arg' not in self.opt.keys():
            
            opener = urllib2.build_opener()
            page = opener.open(self.URL + '/filmwebRecommends/').read()
            matchesYearsRecommended = list(set(re.compile('href="/filmwebRecommends/([0-9]+)"').findall(page)))
            matchesYearsRecommended.sort(reverse=True)
            
            listItem = xbmcgui.ListItem(label=self.year)
            xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=sys.argv[0] + '?site=' + self.opt['site'] + '&arg=' + self.year, listitem=listItem, isFolder=True)    
            
            for key in matchesYearsRecommended:
                listItem = xbmcgui.ListItem(label=key)
                xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=sys.argv[0] + '?site=' + self.opt['site'] + '&arg=' + key, listitem=listItem, isFolder=True)
            
            xbmcplugin.endOfDirectory(int(sys.argv[1]))
        
        else:
        
            # połączenie z adresem URL, pobranie zawartości strony
            opener = urllib2.build_opener()
            page = opener.open(self.URL + '/filmwebRecommends/' + self.opt['arg']).read()
                        
            # pobranie ID
            matchesID = list(set(re.compile('1\.fwcdn\.pl/po/[0-9]+/[0-9]+/([0-9]+)/[0-9]+\.').findall(page)))
                    
            # pobieranie trailerów
            if len(matchesID) != 0:
                import getTrailers
                getTrailers.main().parseTrailer(self, matchesID)
                