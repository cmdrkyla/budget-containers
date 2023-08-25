from datetime import datetime
from sys import modules

from controllers.user import UserController


# Datetime wrappers
def datetime_now(timezone:str=None):
    return datetime.now(timezone)
def datetime_utcnow():
    return datetime.utcnow()


# String to class object (for routing to correct module)
def string_to_class(class_string:str):
    # Turn snake_case to HeadedCamelCase first 
    class_pieces = class_string.split("_")
    model_name = "".join(piece.title() for piece in class_pieces)
    controller_name = model_name + "Controller"
    return getattr(modules[__name__], controller_name)
