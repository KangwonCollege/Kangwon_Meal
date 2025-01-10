from sqlalchemy import String, ForeignKey, Enum
from sqlalchemy.orm import mapped_column, Mapped, relationship
from typing import Optional

from models.database.base import Base
from models.enumeration.meal_type import MealType
from models.database.meal import Meal


class Restaurant(Base):
    __tablename__ = "restaurant"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name = mapped_column(String(32), nullable=True)
    type = mapped_column(Enum(MealType))
    meal: Mapped[list[Meal]] = relationship()

    parent_id: Mapped[int] = mapped_column(ForeignKey("meal_info.id"))
    # parent: Mapped["MealInfo"] = relationship(back_populates="meal")

    @classmethod
    def from_data(cls, meal_type: MealType, meal: list[str], name: Optional[str] = None):
        new_cls = cls(
            name=name,
            type=meal_type
        )
        new_cls.meal.extend([
            Meal(name=x) for x in meal
        ])
        return new_cls
