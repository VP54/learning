import datetime


def get_initial_datetime() -> datetime.datetime:
    minute = 2
    modulo = 15
    _minute = modulo - minute % modulo - 1 + minute
    now = datetime.datetime.now()
    return datetime.datetime(now.year, now.month, now.day, now.hour, _minute, 0, 0)
