from typing import TYPE_CHECKING, List

from fastapi import Request
from sqlalchemy import BIGINT, String
from sqlalchemy.orm import relationship, Mapped, mapped_column
from src.db.models import BaseModel

if TYPE_CHECKING:
    from src.orders.models import Referral, Order
    from src.admin.models import AdminUser


class User(BaseModel):
    __tablename__ = "users"

    user_id: Mapped[int] = mapped_column(BIGINT, unique=True, nullable=False)
    username: Mapped[str] = mapped_column(String(255), nullable=True)

    referrals_from: Mapped["Referral"] = relationship(
        "Referral",
        foreign_keys="Referral.id_from",
        back_populates="referrer",
    )
    referrals_to: Mapped["Referral"] = relationship(
        "Referral",
        foreign_keys="Referral.id_to",
        back_populates="referree",
    )

    orders: Mapped[List["Order"]] = relationship("Order", back_populates="user")
    admin: Mapped["AdminUser"] = relationship(
        "AdminUser", foreign_keys="AdminUser.tg_id", back_populates="user", uselist=False
    )

    async def __admin_repr__(self, request: Request):
        return f"{self.username}"
