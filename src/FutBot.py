''' FutBot Module '''

import datetime
from typing import List
from src.BannerMaker import BannerMaker
from src.util import files as fs, metrics, text
from src.util.date import get_actual_datetime
import src.constants as constants # keys, paths, uri, etc
from src.util.config import Config

# mixins
from src.mixins.social import FutBotInstagramMixin, FutBotTwitterMixin

# TOURNAMENTS CONTROL MODULES
from src.types import Match, Tournament
from src.API_Sports import API_Sports

#sleeping time
SLEEP_TIME = 300

class FutBot(
    FutBotTwitterMixin,
    FutBotInstagramMixin
):
    ''' FutBot class - manage bot behavior '''

    def __init__(self):
        print("\n\n[FutBot] STARTING... - " + str(get_actual_datetime()))
        self.config = Config(constants.file_path.CONFIG)

        # tournaments info
        self.api_sports = API_Sports(constants.uri.API_MATCHES)
        self.banner_maker = BannerMaker(constants.uri.API_TEAMS)

        self.tour_ids = constants.tour_ids
        self.tournaments: List[Tournament] = []
        super.__init__()

    def update(self) -> None:
        ''' Handle bot update functions '''

        self.config.update_config()

        self.update_tournaments()

        super().update()

        print("- Update Flag at {}".format(str(get_actual_datetime())))
    
    def update_tournaments(self) -> None:
        ''' Handle tournaments information '''

        if get_actual_datetime().hour < 9:
            if self.tournaments:
                self.tournaments = []
            return
        if self.api_sports.last_update.date() < get_actual_datetime().date() or not self.api_sports.status:
            self.api_sports.update_info()
        if not self.tournaments:
            for id in self.tour_ids:
                res_tour = self.api_sports.get_tour_by_id(id)
                if res_tour:
                    self.tournaments.append(res_tour)

            if self.tw_get_last_tweet_date() < get_actual_datetime().date():
                tours_tweeted = 0
                for tour in self.tournaments:
                    try:
                        if tour and tour.matches:
                            tour.tweet_id = self.tw_tweet_status_lst(text.tour_to_text.full_info_lst(tour))
                            tours_tweeted += 1
                            print("[TW] Publicando partidos del dia - " + tour.name)
                    except Exception as exception:
                        print("ERROR: update_tournaments()-(1)", exception)
                metrics.increase_metric(metrics.TWEETED_DAY_MATCHES, tours_tweeted)

        else:
            alert_time =  get_actual_datetime() + datetime.timedelta(hours = 1)
            matches_tweeted: List[Match] = []
            for tour in self.tournaments:
                if tour and tour.matches:
                    for match in tour.matches[:]:
                        if match.time > alert_time:
                            break
                        tour.matches.remove(match)
                        try:
                            print('\n[FutBot] Publicando partido -- {} vs {} --'.format(match.team_1.name, match.team_2.name))
                            match_text = text.match_to_text.full_info(match)
                            match_text += self.tw_get_screen_names([match.team_1.account_id, match.team_2.account_id])

                            banners = self.banner_maker.get_banners(match)

                            if self.config.is_activated('tweet_match') and banners:
                                match.tweet_id = self.tw_tweet_status(match_text, banners['horizontal'])
                                matches_tweeted.append(match)
                            if self.config.is_activated('post_story_match') and banners:
                                self.ig_post_story(banners['vertical'])
                        except Exception as e:
                            print("ERROR: update_tournaments()-(2) e=", e)

            if matches_tweeted:
                metrics.increase_metric(metrics.TWEETED_MATCHES, len(matches_tweeted))
                if self.config.is_activated('send_match_message'):
                    self.tw_send_match_messages(matches_tweeted)

def get_team_ids(keys_list: List[str]) -> List[str]:
        ''' Returns list containing team_ids for each key in list given by parameter '''

        res = []
        try:
            data = fs.read_json_file(constants.file_path.CLUB_INFO)
            if data:
                for key in keys_list:
                    if key in data.keys() and data[key]['team_id']:
                        res.append(data[key]['team_id'])
        except Exception as exception:
            print("ERROR: get_teams_ids() - e=" + str(exception))
            res = []
        return res
