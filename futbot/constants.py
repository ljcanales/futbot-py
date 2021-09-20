from os import environ
from datetime import timezone, timedelta

class file_path:
    TEXT_TEMPLATES = './text_templates.json'
    CLUB_INFO = './clubsid.json'

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
