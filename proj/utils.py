from django.conf import settings
from django.utils.dateparse import parse_datetime
import zoneinfo


def string_to_localtime(datetime_text):
    d = parse_datetime(datetime_text)
    return d.replace(tzinfo=zoneinfo.ZoneInfo(settings.TIME_ZONE))
