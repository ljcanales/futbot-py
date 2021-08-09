''' API_Sports Module '''

import requests
from .extractors import extract_tournament
from .util.date import get_actual_datetime
from .types import Tournament

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

    def get_tour_by_id(self, id_event: str) -> Tournament:
        print('[API_Sports] Getting tour (id = {})'.format(id_event))
        tour = None
        try:
            if self.res and self.res['fechas'] and self.res['fechas'][0]:
                for tour_data in self.res['fechas'][0]['torneos']:
                    if tour_data['id'] == id_event:
                        tour = extract_tournament(tour_data)
                        print('[API_Sports]  --  name: {}'.format(tour.name))
                        print('[API_Sports]  --  matches: {}'.format(len(tour.matches)))
                        break
        except Exception as e:
            print("ERROR: API_Sports.get_by_id()", e)
        return tour

    def update_info(self) -> None:
        print("[API_Sports] Updating TOURNAMENTS information")
        try:
            self.res = requests.get(self.api_url).json()
            self.last_update = get_actual_datetime()
            self.status = True
        except Exception as exception:
            self.status = False
            print("ERROR: API_Sports.update_info - e: ", str(exception))
