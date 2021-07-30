import datetime
from src.constants import time

TIME_ZONE = datetime.timezone(datetime.timedelta(hours=-3)) #Argentina UTC-3

def get_actual_datetime() -> datetime.datetime:
    ''' Returns actual datetime by TIME_ZONE '''

    return datetime.datetime.now().astimezone(time.TIME_ZONE)
