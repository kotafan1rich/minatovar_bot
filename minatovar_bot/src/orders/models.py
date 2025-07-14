import enum

from sqlalchemy import (
    BIGINT,
    Column,
    Enum,
    Float,
    ForeignKey,
    Index,
    Integer,
    String,
    UniqueConstraint,
)
from sqlalchemy.orm import relationship
from src.db.models import BaseModel


class OrderStatus(enum.Enum):
    CREATED = "🙋‍♂️ Создан"
    PAID = "💴 Заказ оплачен"
    BOUGHT_OUT = "✈️ Выкуплен"
    AGENT = "👨‍💼 Передан Агенту"
    CUSTOMS = "🛃 Таможня"
    MOSCOW_WAREHOUSE = "📦 на складе в Москве"
    TO_PETERSBURG = "🚚 Едет в Питер"
    TO_CUSTOMER_CITY = "📨 Едет в город к покупателю"
    COMPLETED = "🏠 Завершен"
    CANCELED = "❌ Отменён"


class OrderTypeItem(enum.Enum):
    SHOES = "Обувь"
    CLOTH = "Одежда"


class Referral(BaseModel):
    __tablename__ = "referrals"

    id = Column(Integer, primary_key=True)
    id_from = Column(
        BIGINT, ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False
    )
    id_to = Column(
        BIGINT,
        ForeignKey("users.user_id", ondelete="CASCADE"),
        nullable=False,
        unique=True,
    )

    referrer = relationship(
        "User",
        foreign_keys=[id_from],
        back_populates="referrals_from",
    )
    referree = relationship(
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

    id = Column(Integer, primary_key=True)
    user_id = Column(BIGINT, ForeignKey("users.user_id"), nullable=False)
    status = Column(Enum(OrderStatus), default=OrderStatus.CREATED, nullable=False)
    article = Column(String(255), nullable=False)
    addres = Column(String(255), nullable=False)
    price_rub = Column(Float, nullable=False, default=0.0)
    price_cny = Column(Integer, nullable=False, default=0)
    size = Column(String(100), nullable=False)
    type_item = Column(Enum(OrderTypeItem), default=OrderTypeItem.SHOES, nullable=False)

    user = relationship("User", back_populates="orders")
