# -*- coding: utf-8 -*-

import os
import sys
import xbmc
import xbmcaddon
import xbmcplugin
import xbmcgui

__addon__               = xbmcaddon.Addon()
__addonpath__           = xbmc.translatePath(__addon__.getAddonInfo('path'))
__path_img__            = os.path.join(__addonpath__, 'resources', 'media' )

class main:
    def parse(self, selfGet):
        
        # vars
        self = selfGet
        
        menu = [
        ['Premiery Kino', 'kino', __path_img__ + '//kino.png'],
        ['Premiery DVD', 'dvd', __path_img__ + '//dvd.png'],
        ['Polecane przez Filmweb', 'filmweb', __path_img__ + '//star.png'],
        ['Rankingi', 'top', __path_img__ + '//top.png'],
        ['Chcę zobaczyć', 'wannasee', __path_img__ + '//see.png'],
        ['W moim mieście', 'city', __path_img__ + '//city.png'],
        ['Filmy znajomych', 'friends', __path_img__ + '//user.png'],
        ['Po premierze DVD które chcę zobaczyć', 'afterpremiere', __path_img__ + '//dvd.png']
        ]

        for key in menu:
            listItem = xbmcgui.ListItem(label=key[0], iconImage=key[2])
            xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=sys.argv[0] + '?' + 'site=' + key[1], listitem=listItem, isFolder=True)

        xbmcplugin.endOfDirectory(int(sys.argv[1]))
        