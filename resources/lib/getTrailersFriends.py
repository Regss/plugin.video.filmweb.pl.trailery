# -*- coding: utf-8 -*-

import urllib
import urllib2
import sys
import xbmcplugin
import xbmcgui

import filmweb
import getTrailers

class main:
    def parse(self, selfGet):
        
        # vars
        self = selfGet

        if 'arg' not in self.opt.keys():
        
            friends = filmweb.Filmweb().getUserFriends()
            if friends == False:
                return False
            
            for id in friends.keys():
                login = friends[id]['login']
                name = '' if friends[id]['name'] == '' else ' (' + friends[id]['name'] + ')'
                listItem = xbmcgui.ListItem(label=login + name)
                xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=sys.argv[0] + '?site=' + self.opt['site'] + '&arg=' + str(id), listitem=listItem, isFolder=True)
            xbmcplugin.endOfDirectory(int(sys.argv[1]))
        
        else:
            listID = filmweb.Filmweb().getUserFilmWantToSee(self.opt['arg'])
            if listID == False:
                return False
                
            # pobieranie trailerów
            if len(listID) != 0:
                getTrailers.main().parseTrailer(self, listID)
            