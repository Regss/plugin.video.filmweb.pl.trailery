# -*- coding: utf-8 -*-

import filmweb
import getTrailers

class main:
    def parse(self, selfGet):
        
        # vars
        self = selfGet
        
        listID = filmweb.Filmweb().getUserFilmWantToSee()
        if listID == False:
            return False
            
        # pobieranie trailerów
        if len(listID) != 0:
            getTrailers.main().parseTrailer(self, listID)
        