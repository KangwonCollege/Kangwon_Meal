from sqlalchemy import String, ForeignKey, Enum
from sqlalchemy.orm import mapped_column, Mapped, relationship
from typing import TYPE_CHECKING

from models.database.base import Base
from models.meal_type import MealType
from models.database.meal import Meal


class Restaurant(Base):
    __tablename__ = "restaurant"

    id: Mapped[int] = mapped_column(primary_key=True)
    name = mapped_column(String(32), nullable=True)
    type = mapped_column(Enum(MealType))
    meal: Mapped[list[Meal]] = relationship()

    parent_id: Mapped[int] = mapped_column(ForeignKey("meal_info.id"), nullable=True)
    # parent: Mapped["MealInfo"] = relationship(back_populates="meal")
