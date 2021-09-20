from datetime import datetime, timedelta
from futbot.extractors import extract_tournament
from futbot.util.date import get_actual_datetime
from typing import Dict, List
from futbot.types import Tournament, Match, BotModel
from futbot.constants import TOURNAMENTS_IDS, uri
import requests

class SportsMixin(BotModel):
    __uri: str = None
    __res_data: Dict = None
    __status: bool = False
    __last_update: datetime = None
    __tournaments: List[Tournament] = []
    tours_to_post: List[Tournament] = []
    matches_to_post: List[Match] = []

    def __init__(self, **kwargs):
        self.__uri = uri.API_MATCHES
        super().__init__(**kwargs)

    def update(self):
        if get_actual_datetime().hour < 9:
            if self.__tournaments:
                self.__tournaments.clear()
            return
        if  not self.__status or self.__last_update.date() < get_actual_datetime().date():
            self.__update_res_info()
            self.__update_tours_info()
            self.tours_to_post = self.__tournaments.copy()
        else:
            # check matches
            alert_time =  get_actual_datetime() + timedelta(hours = 1)
            for tour in self.__tournaments:
                if tour and tour.matches:
                    for match in tour.matches[:]:
                        if match.time > alert_time:
                            break
                        self.matches_to_post.append(match)
                        tour.matches.remove(match)

    def __update_tours_info(self):
        if self.__status:
            for id in TOURNAMENTS_IDS:
                res_tour = self.__get_tour_by_id(id)
                if res_tour and res_tour.matches:
                    self.__tournaments.append(res_tour)

    def __update_res_info(self) -> None:
        print("[API_Sports] Updating TOURNAMENTS information")
        try:
            self.__res_data = requests.get(self.__uri).json()
            self.__last_update = get_actual_datetime()
            self.__status = True
        except Exception as exception:
            self.__status = False
            print("ERROR: SportsMixin.update_res_info - e: ", str(exception))

    def __get_tour_by_id(self, id_event: str) -> Tournament:
        print('[API_Sports] Getting tour (id = {})'.format(id_event))
        tour = None
        try:
            if self.__res_data and self.__res_data['fechas'] and self.__res_data['fechas'][0]:
                for tour_data in self.__res_data['fechas'][0]['torneos']:
                    if tour_data['id'] == id_event:
                        tour = extract_tournament(tour_data)
                        print('[API_Sports]  --  name: {}'.format(tour.name))
                        print('[API_Sports]  --  matches: {}'.format(len(tour.matches)))
                        break
        except Exception as e:
            print("ERROR: SportMixin.get_by_id()", e)
        return tour
