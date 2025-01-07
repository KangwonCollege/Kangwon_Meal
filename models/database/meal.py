from sqlalchemy import String, ForeignKey, Enum
from sqlalchemy.orm import mapped_column, Mapped, relationship
from typing import TYPE_CHECKING

from models.database.base import Base
from models.enumeration.meal_type import MealType


if TYPE_CHECKING:
    from .restaurant import Restaurant


class Meal(Base):
    __tablename__ = "meal"

    id: Mapped[int] = mapped_column(primary_key=True)
    name = mapped_column(String(32), nullable=True)

    parent_id: Mapped[int] = mapped_column(ForeignKey("restaurant.id"))
    parent: Mapped["Restaurant"] = relationship(back_populates="meal")
