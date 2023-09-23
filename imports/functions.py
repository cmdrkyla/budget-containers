from datetime import date, datetime
import pytz
from sys import modules

import app
from imports.config import DEFAULT_TIMEZONE, SERVER_TIMEZONE
from controllers.activity import ActivityController
from controllers.container import ContainerController
from controllers.period import PeriodController
from controllers.user import UserController


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


# String to class object (for routing to correct module)
def string_to_class(class_string:str) -> object:
    # Turn snake_case to HeadedCamelCase first 
    class_pieces = class_string.split("_")
    model_name = "".join(piece.title() for piece in class_pieces)
    controller_name = model_name + "Controller"
    try:
        class_object = getattr(modules[__name__], controller_name)
        return class_object
    except AttributeError:
        app.app.logger.debug(f"Invalid module or controller: class_string={class_string}")
        return None