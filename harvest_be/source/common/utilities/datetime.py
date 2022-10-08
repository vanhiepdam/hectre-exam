# -*- coding: utf-8 -*-
from datetime import datetime
from datetime import timedelta

import pytz
from django.conf import settings
from django.utils import timezone


class DateTimeUtil:
    @classmethod
    def now(cls):
        return timezone.now()

    @classmethod
    def get_time_from_now(cls, **kwargs):
        """
        kwargs: Params in timedelta function. eg: minutes=5, hours=1,
        """
        return timezone.now() + timedelta(**kwargs)

    @classmethod
    def to_timezone(cls, dt, tz_name=settings.TIME_ZONE):
        """ Convert datetime to timezone datetime

        Args:
            dt (datetime) - The datetime object
            tz_name (str) - The name of timezone

        Returns:
            datetime - The datetime object with new timezone, invalid timezone
                       name make no effect

        """
        try:
            tz = pytz.timezone(tz_name)
        except pytz.UnknownTimeZoneError:
            return dt

        return dt.astimezone(tz)

    @classmethod
    def convert_ts_to_timezone(cls, timestamp, tz_name=settings.TIME_ZONE, is_millisecond=False):
        if is_millisecond:
            timestamp = int(timestamp / 1000)
        return cls.to_timezone(
            datetime.utcfromtimestamp(timestamp).replace(tzinfo=pytz.UTC),
            tz_name=tz_name
        )
