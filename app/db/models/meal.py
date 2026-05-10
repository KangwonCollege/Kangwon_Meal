from typing import TYPE_CHECKING

from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import mapped_column, Mapped, relationship

from app.db.base import Base

if TYPE_CHECKING:
    from .restaurant import Restaurant


class Meal(Base):
    __tablename__ = "meal"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name = mapped_column(String(32), nullable=True)

    parent_id: Mapped[int] = mapped_column(ForeignKey("restaurant.id"))
    parent: Mapped["Restaurant"] = relationship(back_populates="meal")
