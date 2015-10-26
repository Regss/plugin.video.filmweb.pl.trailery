# -*- coding: utf-8 -*-

import xbmc
import json
import datetime

import filmweb
import getTrailers

class main:
    def parse(self, selfGet):
        
        # vars
        self = selfGet
        
        afterPremiere = []
        date = int(datetime.datetime.now().strftime('%Y%m%d'))
        
        # pobiera id filmów użytkownika z filmwebu
        to_see = filmweb.Filmweb().getUserFilmWantToSee()
        if to_see == False:
            return False
        
        # pobranie tytułów
        toSeeDict = filmweb.Filmweb().getFilmsInfoShort(to_see)
        if toSeeDict == False:
            return False
            
        # sprawdza czy tytuł z filmwebu istnieje w bazie XBMC
        b = ''
        for i, t in toSeeDict.items():
            b = b + '{"operator": "is", "field": "title", "value": "' + t + '"}, '
        jsonVideos = '{"jsonrpc": "2.0", "method": "VideoLibrary.GetMovies", "id": "1", "params": {"filter": {"or": [' + b[0:-2] + ']}}, "properties": ["title"]}'
        jsonGetVideos = xbmc.executeJSONRPC(jsonVideos)
        jsonGetVideos = unicode(jsonGetVideos, 'utf-8', errors='ignore')
        jsonGetVideosResponse = json.loads(jsonGetVideos)
        owned = []
        if 'result' in jsonGetVideosResponse and 'movies' in jsonGetVideosResponse['result']:
            for r in jsonGetVideosResponse['result']['movies']:
                owned.append(r['label'].encode('utf-8'))
        
        # dla nie istniejących w bazie pobiera datę premiery
        for i, t in toSeeDict.items():
            if t not in owned:
                # pobiera datę premiery z filmwebu
                premieredDate = toSeeDict = filmweb.Filmweb().getFilmDatePremiereDVD(i)
                if premieredDate == False:
                    return False
                # sprawdza czy data jest starsza od aktualnej
                if premieredDate <= date:
                    afterPremiere.append(i)
        
        # check new DVD premiere to wanna see and notify
        if 'true' in self.settingsCheckNew:
            if 'service' in self.opt.keys() and self.opt['service'] == '2':
                return afterPremiere
            
        # pobieranie trailerów
        if len(afterPremiere) != 0:
            getTrailers.main().parseTrailer(self, afterPremiere)
        