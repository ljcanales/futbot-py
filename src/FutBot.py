''' FutBot Module '''

import os, datetime, json, re
from typing import List
from instagrapi import Client
from src.BannerMaker import BannerMaker
from src.FutBotSocial.FutBotTwitter import FutBotTwitter
import src.util.files as fs
import src.util.metrics as metrics
from src.util.date import get_actual_datetime
import src.constants as constants # keys, paths, uri, etc
from src.util.config import Config

# TOURNAMENTS CONTROL MODULES
from src.model.Match import Match
from src.model.Tournament import Tournament
from src.API_Sports import API_Sports

#sleeping time
SLEEP_TIME = 300

class FutBot:
    ''' FutBot class - manage bot behavior '''

    def __init__(self):
        print("\n\nSTARTING... - " + str(get_actual_datetime()))
        self.config = Config(constants.file_path.CONFIG)
        self.futbot_twitter = FutBotTwitter() # adsdfasfsfafaaffaf

        self.insta_cl = None

        # tournaments info
        self.api_sports = API_Sports(constants.uri.API_MATCHES)
        self.banner_maker = BannerMaker(constants.uri.API_TEAMS)

        self.tour_ids = constants.tour_ids
        self.tournaments = []

    def login_with_credentials(self):
        print('[IG] Connecting...')
        self.insta_cl = None
        if os.path.exists(constants.file_path.IG_CREDENTIALS):
            try:
                self.insta_cl = Client()
                self.insta_cl.load_settings(constants.file_path.IG_CREDENTIALS)
                self.insta_cl.login(constants.ig_keys.USER_NAME, constants.ig_keys.PASSWORD, relogin=True)
            except:
                print('[IG] Creating new credentials...')
                os.remove(constants.file_path.IG_CREDENTIALS)
                self.insta_cl = Client()
                self.insta_cl.login(constants.ig_keys.USER_NAME, constants.ig_keys.PASSWORD, relogin=True)
                self.insta_cl.dump_settings(constants.file_path.IG_CREDENTIALS)
        else:
            self.insta_cl = Client()
            self.insta_cl.login(constants.ig_keys.USER_NAME, constants.ig_keys.PASSWORD, relogin=True)
            self.insta_cl.dump_settings(constants.file_path.IG_CREDENTIALS)
        print('[IG] Connected')

    def update_bot(self):
        ''' Handle bot update functions '''

        self.config.update_config()

        self.update_tournaments()

        #self.check_mentions()

        print("- Update Flag at {}".format(str(get_actual_datetime())))
    
    def update_tournaments(self):
        ''' Handle tournaments information '''

        if get_actual_datetime().hour < 9:
            if self.tournaments:
                self.tournaments = []
            if self.insta_cl:
                self.insta_cl.logout()
                self.insta_cl = None
            return
        if self.api_sports.last_update.date() < get_actual_datetime.date() or not self.api_sports.status:
            self.api_sports.update_info()
        if not self.insta_cl:
            self.login_with_credentials()
        if not self.tournaments:
            print("--  updating TOURNAMENTS information --")
            for id in self.tour_ids:
                res_tour = self.api_sports.get_tour_by_id(id)
                if res_tour:
                    self.tournaments.append(res_tour)

            if self.futbot_twitter.get_last_tweet_date() < get_actual_datetime().date():
                tours_tweeted = 0
                for tour in self.tournaments:
                    try:
                        if tour and tour.matches:
                            tour.tweet_id = self.futbot_twitter.tweet_status_lst(tour.print_tournament())
                            tours_tweeted += 1
                            print("[TW] Publicando partidos del dia - " + tour.name)
                    except Exception as exception:
                        print("ERROR: update_tournaments()-(1)", exception)
                metrics.increase_metric(metrics.TWEETED_DAY_MATCHES, tours_tweeted)

        else:
            alert_time =  get_actual_datetime() + datetime.timedelta(hours = 1)
            matches_tweeted = []
            for tour in self.tournaments:
                if tour and tour.matches:
                    for match in tour.matches[:]:
                        time_lst = match.time.split(':')
                        match_time = get_actual_datetime().replace(hour = int(time_lst[0]), minute = int(time_lst[1]))
                        
                        if match_time > alert_time:
                            break
                        tour.matches.remove(match)
                        try:
                            match_text = match.print_match()
                            json_keys = [x.replace(" ", "") for x in match.get_equipos()]
                            match_text += self.futbot_twitter.get_screen_names(json_keys)
                            
                            banners = self.banner_maker.get_banners(get_team_ids(json_keys), match)

                            if self.config.is_activated('tweet_match') and banners and banners['horizontal']:
                                match.tweet_id = self.futbot_twitter.tweet_status(match_text, banners['horizontal'])
                                print("[TW] Publicando partido -- " + match.equipo1 + "|" + match.equipo2)
                                matches_tweeted.append(match)
                            if self.config.is_activated('post_story_match') and banners and banners['vertical']:
                                self.post_story(banners['vertical'])
                                print("[IG] Publicando partido -- " + match.equipo1 + "|" + match.equipo2)
                        except Exception as e:
                            print("ERROR: update_tournaments()-(2) e=", e)

            if matches_tweeted:
                metrics.increase_metric(metrics.TWEETED_MATCHES, len(matches_tweeted))
                if self.config.is_activated('send_match_message'):
                    self.futbot_twitter.send_match_messages(matches_tweeted)

    def post_story(self, path):
        try:
            if path:
                self.insta_cl.photo_upload_to_story(path, 'From FutBot')
        except Exception as exception:
            raise Exception(str(exception)) from exception

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
