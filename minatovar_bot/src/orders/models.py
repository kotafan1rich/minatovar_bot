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
            OrderStatus.CANCELED: "❌ Отменён"
        }
        return display_map[self]
        


class OrderTypeItem(enum.Enum):
    SHOES = "SHOES"
    CLOTH = "CLOTH"
    
    def display(self) -> str:
        """Возвращает отображаемое значение на русском языке"""
        display_map = {
            OrderTypeItem.SHOES: "Обувь",
            OrderTypeItem.CLOTH: "Одежда"
        }
        return display_map[self]


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
    status: OrderStatus = Column(
        Enum(OrderStatus), default=OrderStatus.CREATED, nullable=False
    )
    article = Column(String(255), nullable=False)
    addres = Column(String(255), nullable=False)
    price_rub = Column(Float, nullable=False, default=0.0)
    price_cny = Column(Integer, nullable=False, default=0)
    size = Column(String(100), nullable=False)
    type_item: OrderTypeItem = Column(
        Enum(OrderTypeItem), default=OrderTypeItem.SHOES, nullable=False
    )

    user = relationship("User", back_populates="orders")
