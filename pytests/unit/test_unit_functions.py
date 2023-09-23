from datetime import date, datetime
from freezegun import freeze_time
import pytest
import pytz

from imports.functions import *
from models.user import User

class TestFunctionsDatetimeNow():
    def test__datetime_now__no_timezone_provided(self):
        # Currently hardcoded, it should figure out the offset from config values
        # Given - we freeze time in localtime
        frozen_timestring_local = "2023-08-28 15:57:01"
        frozen_datetime_utc = datetime(2023, 8, 28, 19, 57, 1)
        with freeze_time(frozen_timestring_local):
            # When - we request the current time (no timezone)
            current_time = datetime_now()
        
        # Then - the time matches with our offset
        assert current_time.hour == frozen_datetime_utc.hour


    def test__datetime_now__no_timezone_provided_dst(self):
        # Currently hardcoded, it should figure out the offset from config values
        # Given - we freeze time in localtime
        frozen_timestring_local = "2023-08-28 15:57:01"
        frozen_datetime_utc = datetime(2023, 8, 28, 19, 57, 1)
        with freeze_time(frozen_timestring_local):
            # When - we request the current time (no timezone)
            current_time = datetime_now()
        
        # Then - the time matches with our offset
        assert current_time.hour == frozen_datetime_utc.hour


    def test__datetime_now__different_timezone_provided(self):
        # Currently hardcoded, it should figure out the offset from config values
        # Given - we freeze time
        frozen_timestring_edt = "2023-08-28 15:57:01"
        frozen_datetime_cdt = datetime(2023, 8, 28, 14, 57, 1)
        with freeze_time(frozen_timestring_edt):
            # When - we request the current time
            current_time = datetime_now(pytz.timezone("America/Chicago"))
        
        # Then - the time matches with our offset
        assert current_time.hour == frozen_datetime_cdt.hour


    def test__datetime_now__same_timezone_provided(self):
        # Currently hardcoded, it should figure out the offset from config values
        # Given - we freeze time
        frozen_timestring_edt = "2023-08-28 15:57:01"
        frozen_datetime_edt = datetime(2023, 8, 28, 15, 57, 1)
        with freeze_time(frozen_timestring_edt):
            # When - we request the current time
            current_time = datetime_now(pytz.timezone("America/New_York"))
        
        # Then - the time matches (no offset)
        assert current_time.hour == frozen_datetime_edt.hour


class TestFunctionsDatetimeUtcnow():
    def test__datetime_utcnow(self):
        # Given - we freeze time in localtime
        frozen_timestring_local = "2023-01-28 15:57:01"
        frozen_datetime_utc = datetime(2023, 8, 28, 20, 57, 1)
        with freeze_time(frozen_timestring_local):
            # When - we request the current time (no timezone)
            current_time = datetime_utcnow()
        
        # Then - the time matches with our offset
        assert current_time.hour == frozen_datetime_utc.hour


# TODO: Tests for new date_now and date_utcnow functions


class TestFunctionsStringToClass():
    def test__string_to_class__valid(self):
        # Given - a string to turn into a valid class
        class_string = "user"

        # When - we call the function
        class_object = string_to_class(class_string)

        # Then - the user class is returned
        assert class_object.__name__ == "UserController"


    def test__string_to_class__invalid(self):
        # Given - a string to turn into a valid class
        class_string = "invalid_class"

        # When - we call the function
        class_object = string_to_class(class_string)
        
        # Then - the exception is caught and None is returned
        assert class_object == None


    # We don't have a multi-word case to try yet
