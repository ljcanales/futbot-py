''' API_Sports Module '''

import requests, re
from src.model.Tournament import Tournament
from src.model.Match import Match
from src.util.date import get_actual_datetime

class API_Sports():
    api_url = None
    res = None
    status = False
    last_update = None

    def __init__(self, api_url):
        self.api_url = api_url
        try:
            self.res = requests.get(api_url).json()
            self.last_update = get_actual_datetime()
            self.status = True
        except Exception as exception:
            self.status = False
            print("ERROR: API_Sports.init() - e: ", str(exception))

    def get_tour_by_id(self, id_event):
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
                            equipos = re.split('(?:\s*[\w|\s]*final[\w|\s]*[:|-]{1}\s+)|(?:\s*vs.?\s*)|(?:\s*-\s*)|(?:\s*\([\w|\s]*final[\w|\s]*\)\s*)', e['nombre'])
                            equipos = [x for x in equipos if x != '']
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

    def update_info(self):
        try:
            self.res = requests.get(self.api_url).json()
            self.last_update = get_actual_datetime()
            self.status = True
        except Exception as exception:
            self.status = False
            print("ERROR: API_Sports.update_info - e: ", str(exception))
