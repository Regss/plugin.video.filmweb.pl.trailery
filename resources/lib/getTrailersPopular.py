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

        popular = filmweb.Filmweb().getPopularFilms()
        
        if popular == False:
            return False
        
        if len(popular) != 0:
            getTrailers.main().parseTrailer(self, popular)
            