import enum

from typing import TYPE_CHECKING

from fastapi import Request
from sqlalchemy import (
    BIGINT,
    Enum,
    Float,
    ForeignKey,
    Index,
    Integer,
    String,
    UniqueConstraint,
)
from sqlalchemy.orm import relationship, Mapped, mapped_column
from src.db.models import BaseModel

if TYPE_CHECKING:
    from src.client.models import User


class OrderStatus(enum.Enum):
    CREATED = "CREATED"
    PAID = "PAID"
    BOUGHT_OUT = "BOUGHT_OUT"
    AGENT = "AGENT"
    CUSTOMS = "CUSTOMS"
    MOSCOW_WAREHOUSE = "MOSCOW_WAREHOUSE"
    TO_PETERSBURG = "TO_PETERSBURG"
    TO_CUSTOMER_CITY = "TO_CUSTOMER_CITY"
    COMPLETED = "COMPLETED"
    CANCELED = "CANCELED"

    def display(self) -> str:
        """Возвращает отображаемое значение с эмодзи"""
        display_map = {
            OrderStatus.CREATED: "🙋‍♂️ Создан",
            OrderStatus.PAID: "💴 Заказ оплачен",
            OrderStatus.BOUGHT_OUT: "✈️ Выкуплен",
            OrderStatus.AGENT: "👨‍💼 Передан Агенту",
            OrderStatus.CUSTOMS: "🛃 Таможня",
            OrderStatus.MOSCOW_WAREHOUSE: "📦 на складе в Москве",
            OrderStatus.TO_PETERSBURG: "🚚 Едет в Питер",
            OrderStatus.TO_CUSTOMER_CITY: "📨 Едет в город к покупателю",
            OrderStatus.COMPLETED: "🏠 Завершен",
            OrderStatus.CANCELED: "❌ Отменён",
        }
        return display_map[self]

    async def __admin_repr__(self, request: Request):
        return self.display()


class OrderTypeItem(enum.Enum):
    SHOES = "SHOES"
    CLOTH = "CLOTH"

    def display(self) -> str:
        """Возвращает отображаемое значение на русском языке"""
        display_map = {OrderTypeItem.SHOES: "Обувь", OrderTypeItem.CLOTH: "Одежда"}
        return display_map[self]

    async def __admin_repr__(self, request: Request):
        return self.display()


class Referral(BaseModel):
    __tablename__ = "referrals"

    id_from: Mapped[int] = mapped_column(
        BIGINT, ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False
    )
    id_to: Mapped[int] = mapped_column(
        BIGINT,
        ForeignKey("users.user_id", ondelete="CASCADE"),
        nullable=False,
        unique=True,
    )

    referrer: Mapped["User"] = relationship(
        "User",
        foreign_keys=[id_from],
        back_populates="referrals_from",
    )
    referree: Mapped["User"] = relationship(
        "User",
        foreign_keys=[id_to],
        back_populates="referrals_to",
    )

    __table_args__ = (
        UniqueConstraint("id_from", "id_to", name="unique_referral"),
        Index("ix_user_id", "id_from", "id_to"),
    )


class Order(BaseModel):
    __tablename__ = "orders"

    user_id: Mapped[int] = mapped_column(BIGINT, ForeignKey("users.user_id"), nullable=False)
    status: Mapped[OrderStatus] = mapped_column(
        Enum(OrderStatus), default=OrderStatus.CREATED, nullable=False
    )
    article: Mapped[str] = mapped_column(String(255), nullable=False)
    addres: Mapped[str] = mapped_column(String(255), nullable=False)
    price_rub: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    price_cny: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    size: Mapped[str] = mapped_column(String(100), nullable=False)
    type_item: Mapped[OrderTypeItem] = mapped_column(
        Enum(OrderTypeItem), default=OrderTypeItem.SHOES, nullable=False
    )

    user = relationship("User", back_populates="orders")
