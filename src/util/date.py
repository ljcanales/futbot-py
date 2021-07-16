import datetime

TIME_ZONE = datetime.timezone(datetime.timedelta(hours=-3)) #Argentina UTC-3

def get_actual_datetime():
    ''' Returns actual datetime by TIME_ZONE '''

    return datetime.datetime.now().astimezone(TIME_ZONE)
