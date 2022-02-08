from datetime import datetime
import pytz

from .config import TIMEZONE_STR


def get_datetime():
    timezone = pytz.timezone(TIMEZONE_STR)
    return datetime.now(timezone)


def get_date_str():
    now = get_datetime()
    year_str = str(now.year)
    month_str = str(now.month)
    day_str = str(now.day)
    if len(month_str) < 2:
        month_str = '0' + month_str
    if len(day_str) < 2:
        day_str = '0' + day_str
    date_str = f"{year_str}{month_str}{day_str}"
    return date_str


def get_seconds_of_day():
    now = get_datetime()
    return now.hour * 3600 + now.minute * 60 + now.second
