from sqlalchemy import Float, String
from sqlalchemy.orm import mapped_column, Mapped
from src.db.models import BaseModel


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
