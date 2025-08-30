from sqlalchemy import Column, Float, Integer, String
from src.db.models import BaseModel


class Settings(BaseModel):
    __tablename__ = "settings"

    Column(Integer, primary_key=True)
    key = Column(String(255), nullable=False)
    value = Column(Float, nullable=False)


class Promos(BaseModel):
    __tablename__ = "promos"

    descriptions = Column(String(4096), nullable=False)


class AdminUser(BaseModel):
    __tablename__ = "admins"

    username = Column(String(255), nullable=False, unique=True)
    hashed_password = Column(String(255), nullable=False)
