import datetime


class Weekday:
    def __init__(self, date: datetime.date):
        self.date = date

    @property
    def monday() -> datetime.date:
        return self.date + datetime.timedelta(days=-self.date.weekday())

    @property
    def friday() -> datetime.date:
        return self.monday + datetime.timedelta(days=4)

    @property
    def saturday() -> datetime.date:
        return self.monday + datetime.timedelta(days=5)

    @property
    def sunday() -> datetime.date:
        return self.monday + datetime.timedelta(days=6)
