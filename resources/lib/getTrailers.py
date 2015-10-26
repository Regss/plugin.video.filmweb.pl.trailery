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

import filmweb

class main:

    def parseTrailer(self, selfGet, moviesID):
        
        # vars
        self = selfGet
        
        for id in moviesID:
            data = filmweb.Filmweb().getFilmInfoFull(id)
            if data == False:
                return False
            desc = filmweb.Filmweb().getFilmDescription(id)
            if desc == False:
                return False
                
            # check trailer
            if data['trailer'] is not None:
                pattern = ['\.360p\.', '\.480p\.', '\.720p\.']
                trailer = ''
                for p in pattern:
                    for t in data['trailer']:
                        if re.search(p, str(t)):
                            trailer = str(t)
                
                if len(trailer) > 0:
                    
                    # add trailer to playlist
                    listitem=xbmcgui.ListItem(label=data['title'], iconImage=data['poster'], thumbnailImage=data['poster'])
                    listitem.setProperty('IsPlayable', 'true')
                    listitem.setInfo(type='Video', infoLabels={ 'Title': data['title']})
                    listitem.setInfo(type='Video', infoLabels={ 'Originaltitle': data['originaltitle']})
                    listitem.setInfo(type='Video', infoLabels={ 'Year': data['year']})
                    listitem.setInfo(type='Video', infoLabels={ 'Rating': data['rating']})
                    listitem.setInfo(type='Video', infoLabels={ 'Votes': data['votes']})
                    listitem.setInfo(type='Video', infoLabels={ 'Plot': desc})
                    listitem.setInfo(type='Video', infoLabels={ 'Genre': data['genre']})
                    xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=trailer, listitem=listitem, isFolder=False)
                    self.MOVIES.append({'url': trailer, 'title': data['title'], 'item': listitem, 'poster': data['poster']})
                