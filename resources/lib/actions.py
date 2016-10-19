# -*- coding: utf-8 -*-

import xbmc
import xbmcaddon

__addon__               = xbmcaddon.Addon()
__icon__                = __addon__.getAddonInfo('icon')
__addonname__           = __addon__.getAddonInfo('name')

import filmweb
import debug

class main:

    def start(self, opt):
       
        if opt['action'] == 'wantwatch' and 'id' in opt.keys():
            self.markAsWantWatch(opt['id'])
    
        if opt['action'] == 'dontwantwatch' and 'id' in opt.keys():
            self.unmarkAsWantWatch(opt['id'])
            
    def markAsWantWatch(self, ID):
        res = filmweb.Filmweb().addUserFilmWantToSee(ID)
        if res is True:
            debug.notify('Dodano do listy')
        else:
            debug.notify('Błąd w dodawaniu')
            
    def unmarkAsWantWatch(self, ID):
        res = filmweb.Filmweb().removeUserFilmWantToSee(ID)
        if res is True:
            debug.notify('Usunięto do listy')
        else:
            debug.notify('Błąd w usuwaniu')