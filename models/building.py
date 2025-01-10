from enum import Enum
from models.enumeration.school_meal_type import SchoolMealType


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
    
    @property
    def type(self) -> str:
        if self == Building.dorm_1 or self == Building.dorm_2:
            return "dormitory"
        return "school"

    @property
    def school_meal_type(self) -> SchoolMealType:
        if self.type == "dormitory":
            raise NotImplementedError()

        if self == Building.cheonji:
            return SchoolMealType.CheonJi
        elif self == Building.beakrok:
            return SchoolMealType.BaekNok
        elif self == Building.duri:
            return SchoolMealType.Duri

    @classmethod
    def find_key(cls, key: str):
        enum_val = [i for i in list(cls) if i.value == key]
        if len(enum_val) == 0:
            return key
        return enum_val[0]
