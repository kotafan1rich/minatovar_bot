from typing import TYPE_CHECKING

from sqlalchemy import Float, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.db.models import BaseModel

if TYPE_CHECKING:
    from src.client.models import User


class Settings(BaseModel):
    __tablename__ = "settings"

    key: Mapped[str] = mapped_column(String(255), nullable=False)
    value: Mapped[float] = mapped_column(Float, nullable=False)


class Promos(BaseModel):
    __tablename__ = "promos"

    descriptions: Mapped[str] = mapped_column(String(4096), nullable=False)


class AdminUser(BaseModel):
    __tablename__ = "admins"

    username: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    tg_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.user_id"), nullable=True)

    user: Mapped["User"] = relationship(
        "User", foreign_keys=[tg_id], back_populates="admin", uselist=False
    )
