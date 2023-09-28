from datetime import datetime
from freezegun import freeze_time
import pytz

from imports.functions import *

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
