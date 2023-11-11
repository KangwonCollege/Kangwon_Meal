from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String

from models.base import Base


class Meal(Base):
    __tablename__ = "meal"

    name = Column(String(32), nullable=True)
    meal = Column(list)
    time = Column(String(32))


class MealTime(Base):
    __tablename__ = "meal_info"

    breakfast = Column(Integer, nullable=True)
    lunch = Column(Integer, nullable=True)
    dinner = Column(Integer, nullable=True)


class MealInfo(Base):
    __tablename__ = "meal"
    id = Column(Integer, primary_key=True)
    date = Column(Integer)
    building = Column(Integer)
    meal = relationship(
        "meal_info",
        cascade="all,delete-orphan",
        back_populates="submitter",
        uselist=True,
    )


