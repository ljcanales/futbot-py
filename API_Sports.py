''' API_Sports Module '''

import requests
from Tournament import Tournament
from Match import Match

class API_Sports():
    def __init__(self, api_url):
        try:
            self.res = requests.get(api_url).json()
        except Exception:
            self.res = None
            print("ERROR: API_Sports.init()")
    
    def get_by_id(self, id_event):
        tour = Tournament(id_event)
        try:
            if self.res and self.res['fechas'] and self.res['fechas'][0]:
                d = self.res['fechas'][0]['fecha'].split('-')
                tour.set_date(d[2] + "-" + d[1] + "-" + d[0])

                matches = []
                for t in self.res['fechas'][0]['torneos']:
                    if t['id'] == id_event:
                        tour.set_name(t['nombre'])
                        for e in t['eventos']:
                            
                            mat_time = e['fecha'][11:][:5]
                            equipos = e['nombre'].split(' vs ')
                            mat_tv = []
                            for c in e['canales']:
                                mat_tv.append(c['nombre'])
                            
                            match = Match(tour, mat_time, equipos[0], equipos[1], mat_tv)
                            matches.append(match)
                        break
                
                tour.set_matches(matches)
        except Exception as e:
            print("ERROR: API_Sports.get_by_id()", e)
            tour = None
        
        return tour
