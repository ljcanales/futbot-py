import os
from instagrapi import Client
import src.util.metrics as metrics
import src.constants as constants

class FutBotInstagram:
    insta_cl = None

    def __init__(self):
        #self.login()
        pass
    
    def login(self):
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
    
    # def relogin(self):
    #     self.insta_cl.relogin()

    def logout(self):
        self.insta_cl.logout()
        self.insta_cl = None
    
    def is_logged(self):
        if self.insta_cl:
            return True
        return False
    
    def post_story(self, path):
        try:
            if path:
                self.insta_cl.photo_upload_to_story(path, 'From FutBot')
        except Exception as exception:
            raise Exception(str(exception)) from exception
