from datetime import datetime, timedelta

from lxml import html
from futbot.extractors import extract_tournaments_v2
from futbot.util.date import get_actual_datetime
from typing import List
from futbot.types import Tournament, Match, BotModel
from futbot.constants import TOURNAMENTS_IDS, uri
import requests

class SportsMixin(BotModel):
    __uri: str = None
    __res_data: html.HtmlElement = None
    __status: bool = False
    __last_update: datetime = None
    __tournaments: List[Tournament] = []
    tours_to_post: List[Tournament] = []
    matches_to_post: List[Match] = []

    def __init__(self, **kwargs):
        self.__uri = uri.SPORTS_AGENDA
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
            self.__tournaments = extract_tournaments_v2(self.__res_data, TOURNAMENTS_IDS)
            for t in self.__tournaments:
                print(f"[API_Sports] Got tournament {t.id}")
                print(f"[API_Sports]  --  name: {t.name}")
                print(f"[API_Sports]  --  matches: {len(t.matches)}")

    def __update_res_info(self) -> None:
        print("[API_Sports] Updating TOURNAMENTS information")
        try:
            page = requests.get(self.__uri)
            self.__res_data = html.fromstring(page.content)
            self.__last_update = get_actual_datetime()
            self.__status = True
        except Exception as exception:
            self.__status = False
            print("ERROR: SportsMixin.update_res_info - e: ", str(exception))
