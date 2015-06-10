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

    def parseTrailer(self, selfGet, movieLink):
        
        # vars
        self = selfGet
        
        trailersData = {}
        
        for link in movieLink:
            
            opener = urllib2.build_opener()
            moviePage = opener.open(self.URL + link).read()
            
            # movie id
            matchId = re.search('filmId:"?([0-9]+)', moviePage)
            id = matchId.group(1)
            
            match = re.search('href="(/video/zwiastun/[^"]+)"', moviePage)
            if match:
            
                trailersData[id] = {}
                
                # trailer link
                trailersData[id]['link'] = match.group(1)
                opener = urllib2.build_opener()
                
                trailerPage = opener.open(self.URL + match.group(1)).read()
                matchLink = re.search('copies...url:"([^"]+)"', trailerPage)
                trailersData[id]['trailer'] = matchLink.group(1) if matchLink else ''
                
                youtube = re.search('http://www.youtube.com/v/([^"]+)', trailersData[id]['trailer'])
                if youtube:
                    trailersData[id]['trailer'] = 'plugin://plugin.video.youtube/play/?video_id=' + youtube.group(1)
                
                # tytuł
                m = re.search('v:itemreviewed">([^<]+)<', moviePage)
                trailersData[id]['title'] = self.parseHtml.unescape(unicode(m.group(1).strip(), 'utf-8')) if m else ''
                
                # tytuł oryginalny
                m = re.search('s-16 top-5">([^<]+)<', moviePage)
                trailersData[id]['originaltitle'] = self.parseHtml.unescape(unicode(m.group(1).strip(), 'utf-8')) if m else ''
                
                # rok
                m = re.search('halfSize">\(([0-9]+)\)', moviePage)
                trailersData[id]['year'] = m.group(1).strip() if m else ''
                
                # rating
                m = re.search('v:average">([^<]+)<', moviePage)
                trailersData[id]['rating'] = m.group(1).strip().replace(',', '.') if m else ''
                
                # votes
                m = re.search('v:votes">([^<]+)<', moviePage)
                trailersData[id]['votes'] = m.group(1).strip() if m else ''
                
                # plot
                m = re.search('filmPlot bottom-15"><p class="text">([^<]+)<', moviePage)
                trailersData[id]['plot'] = self.parseHtml.unescape(unicode(m.group(1).strip(), 'utf-8')) if m else ''
                
                # director
                m = re.search('v:directedBy">([^<]+)<', moviePage)
                trailersData[id]['director'] = self.parseHtml.unescape(unicode(m.group(1).strip(), 'utf-8')) if m else ''
                
                # genre
                m = re.search('genresList">[^>]+>[^>]+>([^<]+)<', moviePage)
                trailersData[id]['genre'] = self.parseHtml.unescape(unicode(m.group(1).strip(), 'utf-8')) if m else ''
                
                # okładka
                m = re.search('filmPosterLink[^>]+>([^<]+)<', moviePage)
                trailersData[id]['poster'] = m.group(1).replace('.5.', '.3.') if m else ''
                
                # fanart
                m = re.search('data-photo="([^"]+)"', moviePage)
                trailersData[id]['fanart'] = m.group(1) if m else ''
                
                # add trailer to playlist
                listitem=xbmcgui.ListItem(label=trailersData[id]['title'], iconImage=trailersData[id]['poster'], thumbnailImage=trailersData[id]['poster'])
                listitem.setProperty('IsPlayable', 'true')
                listitem.setProperty( 'fanart_image', trailersData[id]['fanart'] )
                listitem.setProperty('IsPlayable', 'true')
                listitem.setInfo(type='Video', infoLabels={ 'Title': trailersData[id]['title']})
                listitem.setInfo(type='Video', infoLabels={ 'Originaltitle': trailersData[id]['originaltitle']})
                listitem.setInfo(type='Video', infoLabels={ 'Year': trailersData[id]['year']})
                listitem.setInfo(type='Video', infoLabels={ 'Rating': trailersData[id]['rating']})
                listitem.setInfo(type='Video', infoLabels={ 'Votes': trailersData[id]['votes']})
                listitem.setInfo(type='Video', infoLabels={ 'Plot': trailersData[id]['plot']})
                listitem.setInfo(type='Video', infoLabels={ 'Director': trailersData[id]['director']})
                listitem.setInfo(type='Video', infoLabels={ 'Genre': trailersData[id]['genre']})
                xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=trailersData[id]['trailer'], listitem=listitem, isFolder=False)
                self.MOVIES.append({'url': trailersData[id]['trailer'], 'title': trailersData[id]['title'], 'item': listitem, 'poster': trailersData[id]['poster']})
                