''' FutBot Module '''

from os import environ
import datetime
import json
from tweepy import OAuthHandler
import tweepy

# TOURNAMENTS CONTROL MODULES
from Match import Match
from Tournament import Tournament
from API_Sports import API_Sports

#load keys
API_KEY = environ['API_KEY']
API_SECRET = environ['API_SECRET']
ACCESS_KEY = environ['ACCESS_KEY']
ACCESS_SECRET = environ['ACCESS_SECRET']

API_MATCHES = environ['API_MATCHES']
API_TEAMS = environ['API_TEAMS']

#mananger user id
MANANGER_USER_ID = environ['MANANGER_USER_ID']

#sleeping time
SLEEP_TIME = 300

TIME_ZONE = datetime.timezone(datetime.timedelta(hours=-3)) #Argentina UTC-3

class FutBot:
    ''' FutBot class - manage bot behavior '''

    def __init__(self):
        self.api_connection = self.create_api()
        self.since_id_dm = 1
        self.last_update_request = datetime.datetime(2018,12,9,17,00).astimezone(TIME_ZONE)
        print("\n\nSTARTING... - " + str(self.get_actual_datetime()))

        # tournaments info
        self.api_sports = API_Sports(API_MATCHES, API_TEAMS)
        self.tour_ids = ['1276', '3']
        self.tournaments = []

    def create_api(self):
        ''' returns the connection to Twitter API '''

        try:
            #authentication
            auth = OAuthHandler(API_KEY, API_SECRET)
            auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
            api_connection = tweepy.API(auth, wait_on_rate_limit = True, wait_on_rate_limit_notify = True)

            return api_connection

        except BaseException as exception:
            print("Error in FutBot.create_api()", exception)
            return None

    def update_bot(self):
        ''' Handle bot update functions '''

        self.direct_message()

        self.update_tournaments()

        print("- Update Flag")

    def direct_message(self):
        ''' Handle direct messages '''

        new_id = self.since_id_dm

        for msg in self.api_connection.list_direct_messages(5):
            if int(msg.id) == self.since_id_dm:
                break
            elif self.since_id_dm == 1: #if it is the first time since last execution
                new_id = int(msg.id)
                break
            new_id = max(int(msg.id), new_id)

            if msg.message_create['sender_id'] == MANANGER_USER_ID:
                self.tweet_status(msg.message_create['message_data']['text'])
                print("tweeting -> ", msg.message_create['message_data']['text'])

        self.since_id_dm = new_id
    
    def update_tournaments(self):
        ''' Handle tournaments information '''

        if self.get_actual_datetime().hour < 9:
            if self.tournaments:
                self.tournaments = []
            return
        if not self.api_sports.status:
            self.api_sports = API_Sports(API_MATCHES, API_TEAMS)
        if not self.tournaments:
            print("--  updating TOURNAMENTS information --")
            for id in self.tour_ids:
                res_tour = self.api_sports.get_by_id(id)
                if res_tour:
                    self.tournaments.append(res_tour)
            self.last_update_request = self.get_actual_datetime()

            for tour in self.tournaments:
                try:
                    if tour and tour.matches and self.get_last_tweet_date() < self.get_actual_datetime().date():
                        self.tweet_status_lst(tour.print_tournament())
                        print("Publicando partidos del dia - " + tour.name)
                except Exception as exception:
                    print("ERROR: update_tournaments()-(1)", exception)

        else:
            alert_time =  self.get_actual_datetime() + datetime.timedelta(hours = 1)
            for tour in self.tournaments:
                if tour and tour.matches:
                    for match in tour.matches[:]:
                        time_lst = match.time.split(':')
                        match_time = self.get_actual_datetime().replace(hour = int(time_lst[0]), minute = int(time_lst[1]))
                        
                        if match_time > alert_time:
                            break
                        try:
                            match_text = match.print_match()
                            json_keys = [x.replace(" ", "") for x in match.get_equipos()]
                            match_text += self.get_screen_names(json_keys)
                            
                            img = self.api_sports.get_img_by_ids(self.get_team_ids(json_keys))

                            self.tweet_status(match_text, img)
                            print("Publicando partido -- " + match.equipo1 + "|" + match.equipo2)
                        except Exception as e:
                            print("ERROR: update_tournaments()-(2) e=", e)

                        tour.matches.remove(match)

    def tweet_status(self, new_status, img_path = None):
        ''' Sends new status with the text given by parameter '''

        try:
            if img_path:
                self.api_connection.update_with_media(status = new_status, filename = img_path)
            else:
                self.api_connection.update_status(status = new_status)
        except Exception as exception:
            raise Exception('Duplicated tweet') from exception
    
    def tweet_status_lst(self, new_status):
        ''' Sends new status with each text in the list given by parameter '''
        reply_id = None
        try:
            for status in new_status:
                reply_id = self.api_connection.update_status(status = status, in_reply_to_status_id = reply_id).id_str
        except Exception as exception:
            raise Exception('Duplicated tweet') from exception

    def get_screen_names(self, keys_list):
        ''' Retuns string containing sreen_names for each key in list given by parameter '''

        res = ""
        try:
            with open("./clubsid.json") as json_file:
                data = json.load(json_file)
                for key in keys_list:
                    if key in data.keys():
                        res += '@' + self.api_connection.get_user(data[key]['account_id']).screen_name + ' '
        except Exception as exception:
            print("ERROR: get_screen_names() - e=" + exception)
            res = ""
        return res
    
    def get_team_ids(self, keys_list):
        ''' Retuns string containing sreen_names for each key in list given by parameter '''

        res = []
        try:
            with open("./clubsid.json") as json_file:
                data = json.load(json_file)
                for key in keys_list:
                    if key in data.keys():
                        res.append(data[key]['team_id'])
        except Exception as exception:
            print("ERROR: get_screen_names() - e=" + exception)
            res = []
        return res

    def get_actual_datetime(self):
        ''' Returns actual datetime by TIME_ZONE '''

        return datetime.datetime.now().astimezone(TIME_ZONE)

    def get_last_tweet_date(self):
        ''' Returns date of last tweet in user timeline '''

        try:
            last_status = self.api_connection.user_timeline(id = self.api_connection.me().id, count = 1)[0]
            return last_status.created_at.astimezone(TIME_ZONE).date()
        except Exception as exception:
            raise Exception("ERROR: get_last_datetime() - e=" + exception) from exception

        return None
