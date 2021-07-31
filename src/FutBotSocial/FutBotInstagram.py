import os
from instagrapi import Client
import src.util.metrics as metrics
from src.constants import file_path, ig_keys

class FutBotInstagram:
    insta_cl: Client = None

    def __init__(self):
        self.login()
        pass

    def update(self):
        pass

    def login(self) -> None:
        print('[IG] Connecting...')
        if self.is_logged():
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

    def logout(self) -> None:
        self.insta_cl.logout()
        self.insta_cl = None
    
    def is_logged(self) -> bool:
        if self.insta_cl:
            return True
        return False
    
    def post_story(self, path: str) -> None:
        try:
            if path:
                print('[IG] Posting story...')
                self.insta_cl.photo_upload_to_story(path, 'From FutBot')
                print('[IG] Story posted')
            else:
                print('[IG] Story path not specified')
        except Exception as exception:
            raise Exception(str(exception)) from exception
