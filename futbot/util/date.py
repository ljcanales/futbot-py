from datetime import (datetime, timedelta, timezone)

TIME_ZONE = timezone(timedelta(hours=-3)) #Argentina UTC-3
WEEK_DAYS = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]

def get_actual_datetime() -> datetime:
    ''' Returns actual datetime by TIME_ZONE '''

    return datetime.now().astimezone(TIME_ZONE)

def string_to_datetime(date_string: str, format_string: str) -> datetime:
    return datetime.strptime(date_string, format_string).replace(tzinfo=TIME_ZONE)
