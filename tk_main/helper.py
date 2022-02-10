from datetime import datetime
import pytz

from .config import Config


class Helper:
    def __init__(self, config: Config):
        self._config = config

    def get_datetime(self):
        timezone = pytz.timezone(self._config.timezone_str())
        return datetime.now(timezone)

    def get_date_int(self):
        now = self.get_datetime()
        year_str = str(now.year)
        month_str = str(now.month)
        day_str = str(now.day)
        if len(month_str) < 2:
            month_str = '0' + month_str
        if len(day_str) < 2:
            day_str = '0' + day_str
        date_int = int(f"{year_str}{month_str}{day_str}")
        return date_int

    def get_seconds_of_day(self):
        now = self.get_datetime()
        return now.hour * 3600 + now.minute * 60 + now.second
