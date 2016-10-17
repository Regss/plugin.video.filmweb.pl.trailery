# -*- coding: utf-8 -*-

import xbmc
import xbmcaddon
import xbmcvfs
import json
import urllib
import urllib2
import hashlib
import os
import re
import datetime

__addon__       = xbmcaddon.Addon()
__addon_id__    = __addon__.getAddonInfo('id')
__addonpath__   = xbmc.translatePath(__addon__.getAddonInfo('path'))
__datapath__    = xbmc.translatePath(os.path.join('special://profile/addon_data/', __addon_id__)).replace('\\', '/') + '/'
__path__        = os.path.join(__addonpath__, 'resources', 'lib' )
__path_img__    = __addonpath__ + '/images/'
__lang__        = __addon__.getLocalizedString

import debug

LOGIN           = __addon__.getSetting('login')
PASS            = __addon__.getSetting('pass')

API_URL         = 'https://ssl.filmweb.pl/api';
API_KEY         = 'qjcGhW2JnvGT9dfCt3uT_jozR3s';
API_ID          = 'android';
API_VER         = '2.2';

class Filmweb:
            
    def getUserFilmWantToSee(self, id='null'):
        
        # pobranie id filmów
        to_see_array = {}
        api_method = 'getUserFilmsWantToSee [' + str(id) + ', null]\n'.encode('string_escape')
        string = self.sendRequest(api_method, 'get')
        if string == False:
            return False
        matches = re.findall(',\[([0-9]+),', string)
        return matches
    
    def getPopularFilms(self):
        # pobranie id filmów
        to_see_array = {}
        api_method = 'getPopularFilms [null, null]\n'.encode('string_escape')
        string = self.sendRequest(api_method, 'get')
        if string == False:
            return False
        matches = re.findall(',([0-9]+)\],', string)
        return matches
        
    def getUserFriends(self):
        tableNames = ['login', '', '', 'name', 'id', '', '', '']
        dictInfo = {}
        api_method = 'getUserFriends [null, null]\n'.encode('string_escape')
        string = self.sendRequest(api_method, 'get')
        if string == False:
            return False
        string = unicode(string, 'utf-8', errors='ignore')
        matches = re.search('(\[.*\])', string.encode('utf-8'))
        infoResponse = json.loads(matches.group(1))
        for data in infoResponse:
            dictInfo[data[4]] = {}
            for i in range(0, len(tableNames)):
                if len(tableNames[i]) > 0:
                    if tableNames[i] == 'name':
                        name = data[i].encode('utf-8') if type(data[i]) == unicode else data[i]
                        name = '' if name == None else name
                        dictInfo[data[4]][tableNames[i]] = name
                    else:
                        dictInfo[data[4]][tableNames[i]] = data[i].encode('utf-8') if type(data[i]) == unicode else data[i]
        return dictInfo
        
    def getFilmsInfoShort(self, listID):
        to_see_array = {}
        if len(listID) > 0:
            id = ','.join(listID)
            api_method = 'getFilmsInfoShort [[' + id + ']]\n'.encode('string_escape')
            string = self.sendRequest(api_method, 'get')
            if string == False:
                return False
            matches = re.findall('\["([^"]+)",[^,]+,[^,]+,[^,]+,[^,]+,[^,]+,([0-9]+)\]', string)
            if len(matches) > 0:
                for m in matches:
                    to_see_array[m[1]] = m[0]
        return to_see_array
    
    def getFilmInfoFull(self, filmwebID):
        tableNames = ['title', 'originaltitle', 'rating', 'votes', 'genre', 'year', 'runtime', '', 'forum', '', '', 'poster', 'trailer', 'premiere_world', 'premiere_poland', '', '', '', 'country', 'outline', '', 'wanna_see', '', '']
        dictInfo = {}
        api_method = 'getFilmInfoFull [' + str(filmwebID) + ']\n'.encode('string_escape')
        string = self.sendRequest(api_method, 'get')
        if string == False:
            return False
        string = unicode(string, 'utf-8', errors='ignore')
        matches = re.search('(\[.*\])', string.encode('utf-8'))
        infoResponse = json.loads(matches.group(1))
        for i in range(0, len(tableNames)):
            if len(tableNames[i]) > 0:
                if tableNames[i] == 'poster':
                    poster = infoResponse[i].encode('utf-8') if type(infoResponse[i]) == unicode else infoResponse[i]
                    poster = '' if poster == None else 'http://1.fwcdn.pl/po' + poster.replace('.2.jpg', '.3.jpg')
                    dictInfo[tableNames[i]] = poster
                else:
                    dictInfo[tableNames[i]] = infoResponse[i].encode('utf-8') if type(infoResponse[i]) == unicode else infoResponse[i]
        return dictInfo
    
    def getFilmDescription(self, filmwebID):
        api_method = 'getFilmDescription [' + str(filmwebID) + ']\n'.encode('string_escape')
        string = self.sendRequest(api_method, 'get')
        if string == False:
            return False
        string = unicode(string, 'utf-8', errors='ignore')
        matches = re.search('(\[.*\])', string.encode('utf-8'))
        infoResponse = json.loads(matches.group(1))
        return '' if infoResponse[0] == None else infoResponse[0].encode('utf-8')
    
    def getFilmPersons(self, filmwebID, t):
        array_type = { 'directors': '1', 'scenarists': '2', 'musics': '3', 'photos': '4', 'actors': '6', 'producers': '9' }
        tableNames = ['id', 'role', 'role_type', 'name', 'img']
        dictPers = {}
        if t in array_type.keys():
            api_method = 'getFilmPersons [' + str(filmwebID) + ', ' + array_type[t] + ', 0, 50]\n'.encode('string_escape')
            string = self.sendRequest(api_method, 'get')
            if string == False:
                return False
            string = unicode(string, 'utf-8', errors='ignore')
            matches = re.search('(\[.*\])', string.encode('utf-8'))
            infoResponse = json.loads(matches.group(1))
            
            for data in infoResponse:
                dictPers[data[0]] = {}
                for i in range(0, len(tableNames)):
                    if tableNames[i] == 'img':
                        dictPers[data[0]][tableNames[i]] = '' if data[i] == None else 'http://1.fwcdn.pl/p' + data[i].encode('utf-8').replace('.1.jpg', '.3.jpg')
                    else:
                        dictPers[data[0]][tableNames[i]] = data[i].encode('utf-8') if type(data[i]) == unicode else data[i]
            return dictPers
        return {}
        
    def getFilmDatePremiereDVD(self, filmwebID):
            req = urllib2.Request('http://www.filmweb.pl/Film?id=' + filmwebID)
            response = urllib2.urlopen(req)
            page = response.read()
            match = re.findall('filmTitle[^<]+<[^<]+href="([^"]+)"', page)
            if len(match) > 0:
                req = urllib2.Request('http://www.filmweb.pl' + match[0] + '/editions')
                response = urllib2.urlopen(req)
                page = response.read()
                match = re.findall('data premiery do sprzedaży: ([0-9]+)-([0-9]+)-([0-9]+)', page)
                if len(match) > 0:
                    date_temp = []
                    for m in match:
                        date_temp.append(int(m[2] + m[1] + m[0]))
                    return min(date_temp)
                else:
                    return 99999999
            else:
                return 99999999
                
    def login(self):

        api_method = 'login [' + LOGIN + ',' + PASS + ',1]\n'.encode('string_escape')
        values = { 'methods': api_method, 'signature': self.create_sig(api_method), 'appId': API_ID, 'version': API_VER }
        data = urllib.urlencode(values)
        
        req = urllib2.Request(API_URL, data)
        try:
            response = urllib2.urlopen(req)
        except Exception as error:
            debug.debug(str(error))
            debug.notify('Błąd połaczenia')
            return False
        
        cookie = response.headers.get('Set-Cookie')
        page = response.read()
        
        debug.debug('Odpowiedź z serwera - ' + page)
        
        if len(re.findall('^err', page)) > 0:
            debug.debug('Błędny login lub hasło')
            debug.notify('Błędny login lub hasło')
            return False
        
        file = open(__datapath__ + 'cookie', 'w')
        file.write(cookie)
        file.close()
        
        debug.debug('Zalogowano')
        return True
        
    def create_sig(self, methods):
        
        return '1.0,' + hashlib.md5(methods + API_ID + API_KEY).hexdigest()
        
    def sendRequest(self, api_method, http_method):
        
        values = { 'methods': api_method, 'signature': self.create_sig(api_method), 'appId': API_ID, 'version': API_VER }
        data = urllib.urlencode(values)
        
        if 'get' in http_method:
            debug.debug(API_URL + '?' + data)
            req = urllib2.Request(API_URL + '?' + data)
        else:
            debug.debug(API_URL + str(data))
            req = urllib2.Request(API_URL, data)
        
        for i in range(0, 2):
        
            if xbmcvfs.exists(__datapath__ + 'cookie') == 0:
                cookie = ''
            else:
                file = open(__datapath__ + 'cookie', 'r')
                cookie = file.read()
                file.close()
        
            req.add_header('cookie', cookie)
            
            try:
                response = urllib2.urlopen(req)
                page = response.read()
                
            except Exception as error:
                page = str(error)
                if i > 0:
                    debug.notify('Błąd połaczenia')
                
            debug.debug('Odpowiedź z serwera - ' + page)
            
            # if not logged go to login and return to request
            matches = re.search('exc UserNotLoggedInException', page)
            matches2 = re.search('HTTP Error 302', page)
            if matches or matches2:
                if self.login() == False:
                    return False
            else:
                break
            
        return page
        