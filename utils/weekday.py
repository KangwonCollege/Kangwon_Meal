import datetime

from typing import NamedTuple


class WeekDayResponse(NamedTuple):
    Monday: datetime.date
    Friday: datetime.date
    Saturday: datetime.date
    Sunday: datetime.date


def weekday(date: datetime.date) -> WeekDayResponse:
    monday_date = date + datetime.timedelta(days=-date.weekday())
    friday_date = monday_date + datetime.timedelta(days=4)
    saturday_date = monday_date + datetime.timedelta(days=5)
    sunday_date = monday_date + datetime.timedelta(days=6)
    return WeekDayResponse(monday_date, friday_date, saturday_date, sunday_date)
