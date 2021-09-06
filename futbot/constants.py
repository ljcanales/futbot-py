from os import environ
from datetime import timezone, timedelta

class file_path:
    CONFIG = './config_file.json'
    TEXT_TEMPLATES = './text_templates.json'
    IG_CREDENTIALS = './ig_credential.json'
    CLUB_INFO = './clubsid.json'

class tw_keys:
    API_KEY = environ['API_KEY']
    API_SECRET = environ['API_SECRET']
    ACCESS_KEY = environ['ACCESS_KEY']
    ACCESS_SECRET = environ['ACCESS_SECRET']

class ig_keys:
    USER_NAME = environ['UN_IG']
    PASSWORD = environ['P_IG']

class uri:
    API_MATCHES = environ['API_MATCHES']
    API_TEAMS = environ['API_TEAMS']

class time:
    TIME_ZONE = timezone(timedelta(hours=-3)) #Argentina UTC-3

TOURNAMENTS_IDS = [
    '1346', # LPA
    '3',    # CL
    '1324', # CA
    '14',   # CARG
    '1247'  # ESQ
]
