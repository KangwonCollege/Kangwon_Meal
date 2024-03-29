from enum import Enum


class Building(Enum):
    cheonji = "CHEONJI"
    beakrok = "BEAKROK"
    duri = "DURI"

    dorm_1 = "DORM_1"
    dorm_2 = "DORM_2"

    def __str__(self):
        if self == Building.cheonji:
            return "천지관"
        elif self == Building.beakrok:
            return "백록관"
        elif self == Building.duri:
            return "두리관"
        elif self == Building.dorm_1:
            return "새롬관"
        elif self == Building.dorm_2:
            return "이룸관"

    @classmethod
    def find_key(cls, key: str):
        enum_val = [i for i in list(cls) if str(i) == key]
        if len(enum_val) == 0:
            return key
        return enum_val[0]
