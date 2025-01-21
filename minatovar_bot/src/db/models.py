import enum

from sqlalchemy import (
    BIGINT,
    Column,
    DateTime,
    Enum,
    Float,
    ForeignKey,
    Index,
    Integer,
    String,
    UniqueConstraint,
    func,
)
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class OrderStatus(enum.Enum):
    CREATED = "Создан"
    WAIT_FOR_PAY = "Ожидает оплаты"
    CONFRIMED = "Подтверждён"
    IN_DILIVER = "В доставке"
    COMPLETED = "Завершён"
    CANCELED = "Отменён"


class OrderTypeItem(enum.Enum):
    SHOES = "Обувь"
    CLOTH = "Одежда"


class User(Base):
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


class Referral(Base):
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


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True)
    user_id = Column(BIGINT, ForeignKey("users.user_id"), nullable=False)
    status = Column(Enum(OrderStatus), default=OrderStatus.CREATED, nullable=False)
    article = Column(String(255), nullable=False)
    addres = Column(String(255), nullable=False)
    price_rub = Column(Float, nullable=False, default=0.0)
    price_cny = Column(Integer, nullable=False, default=0)
    size = Column(Float, nullable=False)
    type_item = Column(Enum(OrderTypeItem), default=OrderTypeItem.SHOES, nullable=False)
    time_created = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="orders")


class Settings(Base):
    __tablename__ = "settings"

    id = Column(Integer, primary_key=True)
    key = Column(String(255), nullable=False)
    value = Column(Float, nullable=False)


class Promos(Base):
    __tablename__ = "promos"

    id = Column(Integer, primary_key=True)
    descriptions = Column(String(4096), nullable=False)
