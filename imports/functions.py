from datetime import date, datetime
import pytz

from imports.config import DEFAULT_TIMEZONE, SERVER_TIMEZONE

# Datetime now wrapper with timezone conversion
def datetime_now(timezone:pytz.BaseTzInfo=None) -> datetime:
    if not timezone:
        timezone = pytz.timezone(DEFAULT_TIMEZONE)
    server_tz = pytz.timezone(SERVER_TIMEZONE)

    # Convert from server time to default time
    now = datetime.now()
    now_server = server_tz.localize(now)
    return now_server.astimezone(timezone).replace(tzinfo=None)


# Same as above, but remove the time
def date_now(timezone:pytz.BaseTzInfo=None) -> date:
    return datetime_now(timezone).date()


# Datetime utcnow wrapper
def datetime_utcnow() -> datetime:
    utc_tz = pytz.timezone("UTC")
    return datetime_now(utc_tz)


# Same as above, but remove the time
def date_utcnow() -> date:
    return datetime_utcnow().date()
