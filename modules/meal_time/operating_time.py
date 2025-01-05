import datetime

from pydantic import BaseModel


class OperatingTime(BaseModel):
    start_hours: int
    start_minutes: int
    end_hours: int
    end_minutes: int

    def start_total_minutes(self) -> int:
        return self.start_hours * 60 + self.start_minutes

    def end_total_minutes(self) -> int:
        return self.end_hours * 60 + self.end_minutes

    def between(self, time: datetime.time) -> bool:
        return self.start_total_minutes() < time.hour * 60 + time.minute < self.end_total_minutes()

    def __ne__(self, other):
        return not self.__eq__(other)

    def __eq__(self, other):
        return (
            self.start_total_minutes() == other.start_total_minutes() and
            self.end_total_minutes() == other.end_total_minutes()
        )

    def __lt__(self, other):
        return self.end_total_minutes() < other.hour * 60 + other.minute

    def __gt__(self, other):
        return self.end_total_minutes() > other.hour * 60 + other.minute

    def __le__(self, other):
        return  self.end_total_minutes() <= other.hour * 60 + other.minute

    def __ge__(self, other):
        return  self.end_total_minutes() >= other.hour * 60 + other.minute
