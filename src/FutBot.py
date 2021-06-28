''' FutBot Module '''

import os
import datetime
import json
import re
from tweepy import OAuthHandler
import tweepy
from instagrapi import Client
from src.util.files import read_json_file
from src.util.files import write_json_file

# TOURNAMENTS CONTROL MODULES
from src.model.Match import Match
from src.model.Tournament import Tournament
from src.API_Sports import API_Sports

#load keys
API_KEY = os.environ['API_KEY']
API_SECRET = os.environ['API_SECRET']
ACCESS_KEY = os.environ['ACCESS_KEY']
ACCESS_SECRET = os.environ['ACCESS_SECRET']
UN_IG = os.environ['UN_IG']
P_IG = os.environ['P_IG']

API_MATCHES = os.environ['API_MATCHES']
API_TEAMS = os.environ['API_TEAMS']
IG_CREDENTIAL_PATH = 'ig_credential.json'

#sleeping time
SLEEP_TIME = 300

TIME_ZONE = datetime.timezone(datetime.timedelta(hours=-3)) #Argentina UTC-3

class FutBot:
    ''' FutBot class - manage bot behavior '''

    def __init__(self):
        self.api_connection = self.create_api()
        self.my_user_id = self.api_connection.me().id
        self.since_id_dm = 1
        self.last_mention_id = 1
        self.last_update_request = datetime.datetime(2018,12,9,17,00).astimezone(TIME_ZONE)
        self.insta_cl = None
        print("\n\nSTARTING... - " + str(get_actual_datetime()))

        # tournaments info
        self.api_sports = API_Sports(API_MATCHES, API_TEAMS)
        self.tour_ids = ['1276', '3', '1324']
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

    def login_with_credentials(self):
        self.insta_cl = None
        if os.path.exists(IG_CREDENTIAL_PATH):
            self.insta_cl = Client()
            self.insta_cl.load_settings(IG_CREDENTIAL_PATH)
            self.insta_cl.login(UN_IG, P_IG)
        else:
            self.insta_cl = Client()
            self.insta_cl.login(UN_IG, P_IG)
            self.insta_cl.dump_settings(IG_CREDENTIAL_PATH)
        print('Log in [IG]')

    def update_bot(self):
        ''' Handle bot update functions '''

        self.update_tournaments()

        self.check_mentions()

        print("- Update Flag")
    
    def update_tournaments(self):
        ''' Handle tournaments information '''

        if get_actual_datetime().hour < 9:
            if self.tournaments:
                self.tournaments = []
                self.api_sports = None
            if self.insta_cl:
                self.insta_cl.logout()
                self.insta_cl = None
            return
        if not self.api_sports or not self.api_sports.status:
            self.api_sports = API_Sports(API_MATCHES, API_TEAMS)
        if not self.insta_cl:
            self.login_with_credentials()
        if not self.tournaments:
            print("--  updating TOURNAMENTS information --")
            for id in self.tour_ids:
                res_tour = self.api_sports.get_by_id(id)
                if res_tour:
                    self.tournaments.append(res_tour)
            self.last_update_request = get_actual_datetime()

            for tour in self.tournaments:
                try:
                    if tour and tour.matches and self.get_last_tweet_date() < get_actual_datetime().date():
                        self.tweet_status_lst(tour.print_tournament())
                        print("Publicando partidos del dia - " + tour.name)
                except Exception as exception:
                    print("ERROR: update_tournaments()-(1)", exception)

        else:
            alert_time =  get_actual_datetime() + datetime.timedelta(hours = 1)
            for tour in self.tournaments:
                if tour and tour.matches:
                    for match in tour.matches[:]:
                        time_lst = match.time.split(':')
                        match_time = get_actual_datetime().replace(hour = int(time_lst[0]), minute = int(time_lst[1]))
                        
                        if match_time > alert_time:
                            break
                        try:
                            match_text = match.print_match()
                            json_keys = [x.replace(" ", "") for x in match.get_equipos()]
                            match_text += self.get_screen_names(json_keys)
                            
                            img = self.api_sports.get_img_by_ids(self.get_team_ids(json_keys))

                            self.tweet_status(match_text, img)
                            print("(TWITTER)Publicando partido -- " + match.equipo1 + "|" + match.equipo2)
                            if img:
                                story_img = self.api_sports.get_vertical_img_by_ids(match)
                                self.post_story(story_img)
                                print("(INSTAGRAM)Publicando partido -- " + match.equipo1 + "|" + match.equipo2)
                        except Exception as e:
                            print("ERROR: update_tournaments()-(2) e=", e)

                        tour.matches.remove(match)
    
    def check_mentions(self):
        presentation = "Hola 👋, mi nombre es FutBot🤖 y te recuerdo los partidos \n\nSeguime y activa las notificaciones🔔"
        follow = " seguime y"
        notification = " activa las notificaciones🔔 para enterarte de cada partido ⚽"
        
        new_id = self.last_mention_id
        for tweet in tweepy.Cursor(self.api_connection.mentions_timeline, since_id = self.last_mention_id).items():
            new_id = max(tweet.id, new_id)
            if self.last_mention_id == 1:
                break
            if tweet.user.id == self.my_user_id:
                continue
            try:
                txt = ""
                if tweet.in_reply_to_user_id  == self.my_user_id:
                    # fijarse si ya respondi el anterior
                    if not tweet.in_reply_to_status_id_str:
                        # es None, creó un nuevo tweet mencionando
                        print("------------in-reply-------------")
                        print("FROM: " + tweet.user.screen_name)
                        print("TEXT: " + tweet.text)
                        print("ANSWER: " + presentation)
                        print("---------------------------------")
                        ## BANNER MAKER V1.1
                        check_vs = split_users_vs(tweet.text)
                        if check_vs:
                            users_img_urls = [self.get_user_photo(u) for u in check_vs]
                            img = self.api_sports.get_banner_by_urls(users_img_urls)
                            if img:
                                self.tweet_status(new_status = '', img_path = img, reply_to = tweet.id)
                        else:
                            self.tweet_status(new_status = presentation, reply_to = tweet.id)
                    else:
                        my_tweet = self.api_connection.get_status(tweet.in_reply_to_status_id_str)
                        # if ERROR tweet deleted
                        txt = "Hola @{},".format(tweet.user.screen_name)
                        if not self.api_connection.lookup_friendships([tweet.user.id])[0].is_followed_by:
                            txt += follow
                        txt += notification
                        if my_tweet.in_reply_to_status_id_str:
                            # si my_tweet es una respuesta
                            if my_tweet.in_reply_to_user_id_str != tweet.user.id_str:
                                # si my_tweet no respondio al mismo usuario
                                print("------------in-replynfslnfsdo-------------")
                                print("FROM: " + tweet.user.screen_name)
                                print("TEXT: " + tweet.text)
                                print("ANSWER: " + txt)
                                print("---------------------------------")
                                self.tweet_status(new_status = txt, reply_to = tweet.id)
                        else:
                            # tweet es una respuesta directa a uno mio
                            # responde a una publicacion
                            print("------------in-reply-------------")
                            print("FROM: " + tweet.user.screen_name)
                            print("TEXT: " + tweet.text)
                            print("ANSWER: " + txt)
                            print("---------------------------------")
                            ## BANNER MAKER V1.1
                            check_vs = split_users_vs(tweet.text)
                            if check_vs:
                                users_img_urls = [self.get_user_photo(u) for u in check_vs]
                                img = self.api_sports.get_banner_by_urls(users_img_urls)
                                if img:
                                    self.tweet_status(new_status = '', img_path = img, reply_to = tweet.id)
                            else:
                                self.tweet_status(new_status = txt, reply_to = tweet.id)
                elif self.my_user_id in [x['id'] for x in tweet.entities['user_mentions']]:
                    # si menciona de onda en respuesta a otro
                    # presentarse
                    print("------------in-mention------------")
                    print("FROM: " + tweet.user.screen_name)
                    print("TEXT: " + tweet.text)
                    print("ANSWER: " + presentation)
                    print("---------------------------------")
                    ## BANNER MAKER V1.1
                    check_vs = split_users_vs(tweet.text)
                    if check_vs:
                        users_img_urls = [self.get_user_photo(u) for u in check_vs]
                        img = self.api_sports.get_banner_by_urls(users_img_urls)
                        if img:
                            self.tweet_status(new_status = '', img_path = img, reply_to = tweet.id)
                    else:
                        self.tweet_status(new_status = presentation, reply_to = tweet.id)
            except Exception as e:
                print(str(e))
                continue
        self.last_mention_id = new_id

    def tweet_status(self, new_status, img_path = None, reply_to = None):
        ''' Sends new status with the text given by parameter '''

        try:
            if img_path:
                self.api_connection.update_with_media(status = new_status, filename = img_path, in_reply_to_status_id = reply_to, auto_populate_reply_metadata = True)
            else:
                self.api_connection.update_status(status = new_status, in_reply_to_status_id = reply_to, auto_populate_reply_metadata = True)
        except Exception as exception:
            raise Exception(str(exception)) from exception
    
    def tweet_status_lst(self, new_status):
        ''' Sends new status with each text in the list given by parameter '''
        reply_id = None
        try:
            for status in new_status:
                reply_id = self.api_connection.update_status(status = status, in_reply_to_status_id = reply_id, auto_populate_reply_metadata = True).id_str
        except Exception as exception:
            raise Exception(str(exception)) from exception

    def get_screen_names(self, keys_list):
        ''' Retuns string containing sreen_names for each key in list given by parameter '''

        res = ""
        try:
            with open("./clubsid.json") as json_file:
                data = json.load(json_file)
                for key in keys_list:
                    if key in data.keys() and data[key]['account_id']:
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
                    if key in data.keys() and data[key]['team_id']:
                        res.append(data[key]['team_id'])
        except Exception as exception:
            print("ERROR: get_screen_names() - e=" + exception)
            res = []
        return res

    def get_last_tweet_date(self):
        ''' Returns date of last tweet in user timeline '''

        try:
            last_status = self.api_connection.user_timeline(id=self.my_user_id, count=1, exclude_replies=True, exclude_rts=True,)[0]
            return last_status.created_at.astimezone(TIME_ZONE).date()
        except Exception as exception:
            raise Exception("ERROR: get_last_datetime() - e=" + str(exception)) from exception

        return None
    
    def get_user_photo(self, user):
        try:
            return self.api_connection.get_user(user.replace('@','')).profile_image_url_https.replace('_normal','')
        except:
            return None

    def post_story(self, path):
        try:
            if path:
                self.insta_cl.photo_upload_to_story(path, 'From FutBot')
        except Exception as exception:
            raise Exception(str(exception)) from exception

def get_actual_datetime():
    ''' Returns actual datetime by TIME_ZONE '''

    return datetime.datetime.now().astimezone(TIME_ZONE)

def split_users_vs(msg):
    result = re.findall("@\w*\s+vs.?\s+@\w*", msg)
    users = []
    
    if result:
        users = re.split("\s+vs.?\s+" , result[0])
    
    return users