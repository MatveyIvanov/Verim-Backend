from datetime import datetime
import pytz

from config import settings


def get_current_time() -> datetime:
    return datetime.now(tz=pytz.timezone(settings.TIMEZONE))
