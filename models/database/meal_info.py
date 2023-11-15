import datetime

from sqlalchemy import Date, Enum
from sqlalchemy.orm import relationship, mapped_column, Mapped

from models.building import Building
from models.database.restaurant import Restaurant
from .base import Base


class MealInfo(Base):
    __tablename__ = "meal_info"

    id: Mapped[int] = mapped_column(primary_key=True)
    date: Mapped[datetime.date] = mapped_column(Date)
    building = mapped_column(Enum(Building))

    breakfast: Mapped[list["Restaurant"]] = relationship(
        primaryjoin="and_(MealInfo.id==Restaurant.parent_id, " "Restaurant.type=='breakfast')")
    lunch: Mapped[list["Restaurant"]] = relationship(
        primaryjoin="and_(MealInfo.id==Restaurant.parent_id, " "Restaurant.type=='lunch')")
    dinner: Mapped[list["Restaurant"]] = relationship(
        primaryjoin="and_(MealInfo.id==Restaurant.parent_id, " "Restaurant.type=='dinner')")
