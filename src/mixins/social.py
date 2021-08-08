import os, re
from instagrapi import Client
from tweepy import OAuthHandler
import tweepy
import src.util.metrics as metrics
from src.constants import file_path, ig_keys, tw_keys, time

from typing import List
from src.types import Match, BotModel

from src.BannerMaker import BannerMaker
import src.util.files as fs

class FutBotInstagramMixin(BotModel):
    insta_cl: Client = None

    def __init__(self):
        self.ig_login()
        super.__init__()
        pass

    def update(self):
        super().update()
        pass

    def ig_login(self) -> None:
        print('[IG] Connecting...')
        if self.ig_is_logged():
            print('[IG] already logged!')
            return
        if os.path.exists(file_path.IG_CREDENTIALS):
            print('[IG] Credentials found...')
            try:
                self.insta_cl = Client()
                self.insta_cl.load_settings(file_path.IG_CREDENTIALS)
                self.insta_cl.login(ig_keys.USER_NAME, ig_keys.PASSWORD, relogin=True)
                print('[IG] Logged in with saved credentials...')
            except:
                print('[IG] Creating new credentials...')
                os.remove(file_path.IG_CREDENTIALS)
                self.insta_cl = Client()
                self.insta_cl.login(ig_keys.USER_NAME, ig_keys.PASSWORD, relogin=True)
                self.insta_cl.dump_settings(file_path.IG_CREDENTIALS)
        else:
            print('[IG] Credentials not found...')
            print('[IG] Creating new credentials...')
            self.insta_cl = Client()
            self.insta_cl.login(ig_keys.USER_NAME, ig_keys.PASSWORD, relogin=True)
            self.insta_cl.dump_settings(file_path.IG_CREDENTIALS)
        print('[IG] Connected')

    def ig_logout(self) -> None:
        self.insta_cl.logout()
        self.insta_cl = None
    
    def ig_is_logged(self) -> bool:
        if self.insta_cl:
            return True
        return False
    
    def ig_post_story(self, path: str) -> None:
        try:
            if path:
                print('[IG] Posting story...')
                self.insta_cl.photo_upload_to_story(path, 'From FutBot')
                print('[IG] Story posted')
            else:
                print('[IG] Story path not specified')
        except Exception as exception:
            raise Exception(str(exception)) from exception

class FutBotTwitterMixin(BotModel):
    _api_connection: tweepy.API = None
    _since_id_dm: int = 1
    _last_mention_id: int = 1
    _my_user_id: int = None

    def __init__(self) -> None:
        print('[TW] Connecting...')
        try:
            #authentication
            auth = OAuthHandler(tw_keys.API_KEY, tw_keys.API_SECRET)
            auth.set_access_token(tw_keys.ACCESS_KEY, tw_keys.ACCESS_SECRET)
            self._api_connection = tweepy.API(auth, wait_on_rate_limit = True, wait_on_rate_limit_notify = True)
            self._my_user_id = self._api_connection.me().id
            print('[TW] Connected')
        except BaseException as exception:
            print("Error in FutBotTwitter.__init__()", str(exception))
        super.__init__()
    
    def update(self) -> None:
        #self.__tw_check_mentions()
        super().update()
        pass
    
    def tw_tweet_status(self, new_status: str, img_path: str = None, reply_to: str = None) -> str:
        ''' Sends new status with the text given by parameter. Return status id_str '''

        try:
            print('[TW] Tweeting status...')
            status_id = None
            if img_path:
                status_id = self._api_connection.update_with_media(status = new_status, filename = img_path, in_reply_to_status_id = reply_to, auto_populate_reply_metadata = True).id_str
            else:
                status_id = self._api_connection.update_status(status = new_status, in_reply_to_status_id = reply_to, auto_populate_reply_metadata = True).id_str
            print('[TW] Status tweeted')
            return status_id
        except Exception as exception:
            raise Exception(str(exception)) from exception

    def tw_tweet_status_lst(self, new_status: List[str]) -> str:
        ''' Sends new status with each text in the list given by parameter '''

        reply_id = None
        first_id = None
        try:
            for status in new_status:
                if reply_id:
                    reply_id = self._api_connection.update_status(status = status, in_reply_to_status_id = reply_id, auto_populate_reply_metadata = True).id_str
                else:
                    first_id = reply_id = self._api_connection.update_status(status = status, in_reply_to_status_id = reply_id, auto_populate_reply_metadata = True).id_str
            return first_id
        except Exception as exception:
            raise Exception(str(exception)) from exception

    def tw_send_match_messages(self, matches: List[Match]) -> None:
        ''' Sends match info to every follower '''

        templates = fs.read_json_file(file_path.TEXT_TEMPLATES)
        cant_templates = 0

        if templates and len(templates['match_message']) > 0:
            templates = templates['match_message']
            cant_templates = len(templates)
        else:
            print('Message templates not found, check text_templates.json file')
            return None
        
        sent_messages = 0
        
        try:
            for follower in tweepy.Cursor(self._api_connection.followers,'FutBot_').items():
                for match in matches:
                    #text = 'Hola @{}\n\n'.format(follower.screen_name)
                    text = ''
                    text += match.message_by_template(templates[sent_messages % cant_templates])
                    if match.tweet_id:
                        text += '\nhttps://twitter.com/FutBot_/status/{}'.format(str(match.tweet_id))
                    self._api_connection.send_direct_message(follower.id_str, text)
                    sent_messages += 1
        except Exception as exception:
            print("ERROR: tw_send_match_messages() - e=" + str(exception))
        finally:
            metrics.increase_metric(metrics.SENT_MATCHES, sent_messages)
    
    def tw_get_screen_names(self, account_id_list: List[str]) -> str:
        ''' Returns string containing sreen_names for each key in list given by parameter '''

        res = ''
        try:
            for account_id in account_id_list:
                if account_id:
                    res += '@' + self._api_connection.get_user(account_id).screen_name + ' '
        except Exception as exception:
            print("ERROR: tw_get_screen_names() - e=" + str(exception))
        return res
    
    def tw_get_last_tweet_date(self):
        ''' Returns date of last tweet in user timeline '''

        try:
            last_status = self._api_connection.user_timeline(id=self._my_user_id, count=1, exclude_replies=True, exclude_rts=True,)[0]
            return last_status.created_at.astimezone(time.TIME_ZONE).date()
        except Exception as exception:
            raise Exception("ERROR: get_last_datetime() - e=" + str(exception)) from exception

        return None
    
    def tw_get_user_photo(self, user: str) -> str:
        try:
            return self._api_connection.get_user(user.replace('@','')).profile_image_url_https.replace('_normal','')
        except:
            return None
    
    def __tw_check_mentions(self) -> None:
        presentation = "Hola 👋, mi nombre es FutBot🤖 y te recuerdo los partidos \n\nSeguime y activa las notificaciones🔔"
        follow = " seguime y"
        notification = " activa las notificaciones🔔 para enterarte de cada partido ⚽"
        
        new_id = self._last_mention_id
        for tweet in tweepy.Cursor(self._api_connection.mentions_timeline, since_id = self._last_mention_id).items():
            new_id = max(tweet.id, new_id)
            if self._last_mention_id == 1:
                break
            if tweet.user.id == self._my_user_id:
                continue
            try:
                txt = ""
                if tweet.in_reply_to_user_id  == self._my_user_id:
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
                            users_img_urls = [self.tw_get_user_photo(u) for u in check_vs]
                            img = BannerMaker.get_banner_by_urls(users_img_urls)
                            if img:
                                self.tw_tweet_status(new_status = '', img_path = img, reply_to = tweet.id)
                        else:
                            self.tw_tweet_status(new_status = presentation, reply_to = tweet.id)
                    else:
                        my_tweet = self._api_connection.get_status(tweet.in_reply_to_status_id_str)
                        # if ERROR tweet deleted
                        txt = "Hola @{},".format(tweet.user.screen_name)
                        if not self._api_connection.lookup_friendships([tweet.user.id])[0].is_followed_by:
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
                                self.tw_tweet_status(new_status = txt, reply_to = tweet.id)
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
                                users_img_urls = [self.tw_get_user_photo(u) for u in check_vs]
                                img = BannerMaker.get_banner_by_urls(users_img_urls)
                                if img:
                                    self.tw_tweet_status(new_status = '', img_path = img, reply_to = tweet.id)
                            else:
                                self.tw_tweet_status(new_status = txt, reply_to = tweet.id)
                elif self._my_user_id in [x['id'] for x in tweet.entities['user_mentions']]:
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
                        users_img_urls = [self.tw_get_user_photo(u) for u in check_vs]
                        img = BannerMaker.get_banner_by_urls(users_img_urls)
                        if img:
                            self.tw_tweet_status(new_status = '', img_path = img, reply_to = tweet.id)
                    else:
                        self.tw_tweet_status(new_status = presentation, reply_to = tweet.id)
            except Exception as e:
                print(str(e))
                continue
        self._last_mention_id = new_id

def split_users_vs(msg: str) -> List[str]:
    result = re.findall("@\w*\s+vs.?\s+@\w*", msg)
    users = []
    
    if result:
        users = re.split("\s+vs.?\s+" , result[0])
    
    return users