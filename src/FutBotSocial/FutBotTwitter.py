import re
from typing import List
from tweepy import OAuthHandler
import tweepy
from src.model.Match import Match
from src.BannerMaker import BannerMaker
import src.constants as constants
import src.util.files as fs
import src.util.metrics as metrics

class FutBotTwitter:
    _api_connection = None
    _since_id_dm = 1
    _last_mention_id = 1
    _my_user_id = None

    def __init__(self):
        print('[TW] Connecting...')
        try:
            #authentication
            auth = OAuthHandler(constants.tw_keys.API_KEY, constants.tw_keys.API_SECRET)
            auth.set_access_token(constants.tw_keys.ACCESS_KEY, constants.tw_keys.ACCESS_SECRET)
            self._api_connection = tweepy.API(auth, wait_on_rate_limit = True, wait_on_rate_limit_notify = True)
            self._my_user_id = self._api_connection.me().id
            print('[TW] Connected')
        except BaseException as exception:
            print("Error in FutBotTwitter.__init__()", str(exception))
    
    def update(self) -> None:
        # self._check_mentions()
        pass
    
    def tweet_status(self, new_status: str, img_path: str = None, reply_to: str = None) -> str:
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

    def tweet_status_lst(self, new_status: List[str]) -> str:
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

    def send_match_messages(self, matches: List[Match]) -> None:
        ''' Sends match info to every follower '''

        templates = fs.read_json_file(constants.file_path.TEXT_TEMPLATES)
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
            print("ERROR: send_match_messages() - e=" + str(exception))
        finally:
            metrics.increase_metric(metrics.SENT_MATCHES, sent_messages)
    
    def get_screen_names(self, account_id_list: List[str]) -> str:
        ''' Returns string containing sreen_names for each key in list given by parameter '''

        res = ''
        try:
            for account_id in account_id_list:
                if account_id:
                    res += '@' + self._api_connection.get_user(account_id).screen_name + ' '
        except Exception as exception:
            print("ERROR: get_screen_names() - e=" + str(exception))
        return res
    
    def get_last_tweet_date(self):
        ''' Returns date of last tweet in user timeline '''

        try:
            last_status = self._api_connection.user_timeline(id=self._my_user_id, count=1, exclude_replies=True, exclude_rts=True,)[0]
            return last_status.created_at.astimezone(constants.time.TIME_ZONE).date()
        except Exception as exception:
            raise Exception("ERROR: get_last_datetime() - e=" + str(exception)) from exception

        return None
    
    def get_user_photo(self, user: str) -> str:
        try:
            return self._api_connection.get_user(user.replace('@','')).profile_image_url_https.replace('_normal','')
        except:
            return None
    
    def _check_mentions(self) -> None:
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
                            users_img_urls = [self.get_user_photo(u) for u in check_vs]
                            img = BannerMaker.get_banner_by_urls(users_img_urls)
                            if img:
                                self.tweet_status(new_status = '', img_path = img, reply_to = tweet.id)
                        else:
                            self.tweet_status(new_status = presentation, reply_to = tweet.id)
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
                                img = BannerMaker.get_banner_by_urls(users_img_urls)
                                if img:
                                    self.tweet_status(new_status = '', img_path = img, reply_to = tweet.id)
                            else:
                                self.tweet_status(new_status = txt, reply_to = tweet.id)
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
                        users_img_urls = [self.get_user_photo(u) for u in check_vs]
                        img = BannerMaker.get_banner_by_urls(users_img_urls)
                        if img:
                            self.tweet_status(new_status = '', img_path = img, reply_to = tweet.id)
                    else:
                        self.tweet_status(new_status = presentation, reply_to = tweet.id)
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
