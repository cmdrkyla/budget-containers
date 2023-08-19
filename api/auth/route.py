from flask import abort
from functools import wraps

from auth.auth import Auth


# Secure routes (must be logged in)
# @wrap fix: https://stackoverflow.com/questions/54457772/
def secure_route(func):
  @wraps(func)
  def wrapper(**args):
      if Auth().is_authenticated():
        return func(**args)
      else:
         abort(403)
  return wrapper
