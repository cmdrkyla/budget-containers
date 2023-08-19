from datetime import datetime
from sys import modules

# Models (all must be listed for routing)
# Could possibly change to dynamic later


# Datetime wrappers
def datetime_now(timezone:str=None):
    return datetime.now(timezone)
def datetime_utcnow():
    return datetime.utcnow()


# String to class object (for routing to correct module)
def string_to_class(class_string:str):
    # Turn snake_case to HeadedCamelCase first 
    class_pieces = class_string.split("_")
    class_name = "".join(piece.title() for piece in class_pieces)
    return getattr(modules[__name__], class_name)