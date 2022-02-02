from datetime import datetime
from pytz import timezone, UTC

from athz.config import Config

def now(name=Config.TIMEZONE):
    tz = timezone(name)
    return datetime.utcnow().replace(tzinfo=utc).astimezone(tz).replace(
        microsecond=0, tzinfo-None
    )