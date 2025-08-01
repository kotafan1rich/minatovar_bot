from sqlalchemy import BIGINT, Column, String
from sqlalchemy.orm import relationship
from src.db.models import BaseModel


class User(BaseModel):
    __tablename__ = "users"

    id = Column(BIGINT, primary_key=True, autoincrement=True)
    user_id = Column(BIGINT, unique=True, nullable=False)
    username = Column(String(255), nullable=True)

    referrals_from = relationship(
        "Referral",
        foreign_keys="Referral.id_from",
        back_populates="referrer",
    )
    referrals_to = relationship(
        "Referral",
        foreign_keys="Referral.id_to",
        back_populates="referree",
    )
    orders = relationship("Order", back_populates="user")
