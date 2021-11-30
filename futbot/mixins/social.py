import re
from instagrapi import Client
import tweepy
from futbot.constants import time

from typing import List
from futbot.types import Match, BotModel

from futbot.BannerMaker import BannerMaker
from futbot.util.text import match_to_text

class FutBotInstagramMixin(BotModel):
    insta_cl: Client = None

    def __init__(self, **kwargs):
        try:
            print('[IG] Connecting...')
            required_args = ['username','password', 'settings']
            if not set(kwargs['instagram'].keys()) <= set(required_args):
                raise Exception('instagram settings not specified')
            if 'instagram' in kwargs.keys() and 'settings' in kwargs['instagram'].keys():
                print('[IG] Credentials found...')
                # try:
                self.insta_cl = Client(settings=kwargs['instagram']['settings'])
                self.insta_cl.login(kwargs['instagram']['username'], kwargs['instagram']['password'], relogin=True)
                print('[IG] Logged in with saved credentials...')
                # except:
                #     print('[IG] Creating new credentials...')
                #     self.insta_cl = Client()
                #     self.insta_cl.login(kwargs['instagram']['username'], kwargs['instagram']['password'], relogin=True)
            else:
                print('[IG] Credentials not found...')
                print('[IG] Creating new credentials...')
                self.insta_cl = Client()
                self.insta_cl.login(kwargs['instagram']['username'], kwargs['instagram']['password'], relogin=True)
            print('[IG] Connected')
        except Exception as exception:
            print("Error in FutBotInstagramMixin.__init__() ", str(exception))
        super().__init__(**kwargs)

    def update(self):
        super().update()
        pass

    def ig_logout(self) -> None:
        self.insta_cl.logout()
        self.insta_cl = None
    
    def ig_is_logged(self) -> bool:
        if self.insta_cl:
            return True
        return False
    
    def ig_get_settings(self) -> dict:
        if self.insta_cl:
            return self.insta_cl.get_settings().copy()
        return {}
    
    def ig_post_story(self, path: str) -> bool:
        try:
            if path:
                print('[IG] Posting story...')
                self.insta_cl.photo_upload_to_story(path, 'From FutBot')
                print('[IG] Story posted')
                return True
            else:
                print('[IG] Story path not specified')
        except Exception as exception:
            #raise Exception(str(exception)) from exception
            pass
        return False

class FutBotTwitterMixin(BotModel):
    _api_connection: tweepy.API = None
    _since_id_dm: int = 1
    _last_mention_id: int = 1
    _my_user_id: int = None

    def __init__(self, **kwargs) -> None:
        print('[TW] Connecting...')
        try:
            required_args = ['api_key','api_secret','access_key','access_secret']
            if 'twitter' in kwargs.keys() and set(kwargs['twitter'].keys()) <= set(required_args):
                #authentication
                auth = tweepy.OAuthHandler(kwargs['twitter']['api_key'], kwargs['twitter']['api_secret'])
                auth.set_access_token(kwargs['twitter']['access_key'], kwargs['twitter']['access_secret'])
                self._api_connection = tweepy.API(auth, wait_on_rate_limit = True)
                self._my_user_id = self._api_connection.me().id
                print('[TW] Connected')
            else:
                raise Exception('twitter settings not specified')
        except BaseException as exception:
            print("Error in FutBotTwitter.__init__() ", str(exception))
        super().__init__(**kwargs)
    
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

    def tw_send_match_messages(self, matches: List[Match]) -> int:
        ''' Sends match info to every follower '''

        sent_messages: int = 0

        try:
            for follower in tweepy.Cursor(self._api_connection.followers,'FutBot_').items():
                for match in matches:
                    text = 'Hola @{}\n\n'.format(follower.screen_name)
                    text += match_to_text.message_info(match)
                    if match.tweet_id:
                        text += '\nhttps://twitter.com/FutBot_/status/{}'.format(str(match.tweet_id))
                    self._api_connection.send_direct_message(follower.id_str, text)
                    sent_messages += 1
        except Exception as exception:
            print("ERROR: tw_send_match_messages() - e=" + str(exception))
        finally:
            return sent_messages

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
            last_status = self._api_connection.user_timeline(id=self._my_user_id, count=1, exclude_replies=True, include_rts=False,)[0]
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
                    # check if already answered
                    if not tweet.in_reply_to_status_id_str:
                        # it's a new tweet with mention
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
                        my_tweet = self._api_connection.get_status(tweet.in_reply_to_status_id_str) # if this raise Exception, it's a deleted tweet
                        txt = "Hola @{},".format(tweet.user.screen_name)
                        if not self._api_connection.lookup_friendships([tweet.user.id])[0].is_followed_by:
                            txt += follow
                        txt += notification
                        if my_tweet.in_reply_to_status_id_str: # if my_tweet is a reply
                            if my_tweet.in_reply_to_user_id_str != tweet.user.id_str: # if my_tweet not replying same user
                                self.tw_tweet_status(new_status = txt, reply_to = tweet.id)
                        else:
                            # tweet is replying bot tweet directly
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
                    # if mention
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
