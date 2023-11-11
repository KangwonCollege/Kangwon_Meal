from sqlalchemy import String, ForeignKey, Enum
from sqlalchemy.orm import mapped_column, Mapped, relationship
from typing import TYPE_CHECKING

from models.database.base import Base
from models.meal_type import MealType


if TYPE_CHECKING:
    from .meal_info import MealInfo


class Meal(Base):
    __tablename__ = "meal"

    id: Mapped[int] = mapped_column(primary_key=True)
    name = mapped_column(String(32), nullable=True)
    type = mapped_column(Enum(MealType))

    parent_id: Mapped[int] = mapped_column(ForeignKey("meal_info.id"))
    # parent: Mapped["MealInfo"] = relationship(back_populates="meal")
