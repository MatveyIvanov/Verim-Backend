from datetime import datetime
import pytz

from config import settings


def get_current_time() -> datetime:
    return datetime.now(tz=pytz.timezone(settings.TIMEZONE))


def timestamp_to_datetime(timestamp: str) -> datetime:
    return datetime.fromtimestamp(timestamp, tz=pytz.timezone(settings.TIMEZONE))
