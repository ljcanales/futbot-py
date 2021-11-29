from datetime import (datetime, timedelta, timezone)
from re import split

TIME_ZONE = timezone(timedelta(hours=-3)) #Argentina UTC-3
WEEK_DAYS = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
MONTHS = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]

def get_actual_datetime() -> datetime:
    ''' Returns actual datetime by TIME_ZONE '''

    return datetime.now().astimezone(TIME_ZONE)

def string_to_datetime(date_string: str, format_string: str) -> datetime:
    return datetime.strptime(date_string, format_string).replace(tzinfo=TIME_ZONE)

def day_month_year_to_datetime(date_string: str) -> datetime:
    data = split(r"\sdel?\s", date_string)
    return datetime(
        year = int(data[2]),
        month = MONTHS.index(data[1]) + 1,
        day = int(data[0]),
        tzinfo = TIME_ZONE
    )
