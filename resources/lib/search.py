# -*- coding: utf-8 -*-

import urllib
import urllib2
import sys
import xbmcplugin
import xbmcgui
import xbmc
import re

import filmweb
import getTrailers

class main:
    def parse(self, selfGet):
        
        # vars
        self = selfGet

        search = xbmc.Keyboard ('', 'Szukaj')
        search.doModal()
        if (search.isConfirmed()):
            searchText = search.getText()
        else:
            return
        
        # połączenie z adresem URL, pobranie zawartości strony
        opener = urllib2.build_opener()
        page = opener.open(self.URL + '/search/live?q=' + urllib.quote(searchText)).read()
        
        # pobranie ID
        matchesID = list(set(re.compile('f\\\c([0-9]+)').findall(page)))
        
        if matchesID == False:
            return False
        
        if len(matchesID) != 0:
            getTrailers.main().parseTrailer(self, matchesID)
            