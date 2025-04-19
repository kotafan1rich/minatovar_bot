from typing import Union

from cache.redis import build_key, cached
from sqlalchemy import delete, exists, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from db.models import Order, OrderStatus, Promos, Referral, Settings, User


class BaseDAL:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session


class SettingsDAL(BaseDAL):
    async def param_exists(self, key: str) -> bool:
        async with self.db_session.begin():
            query = select(exists().where(Settings.key == key))
            res = await self.db_session.execute(query)
            return res.scalar()

    async def update_param(self, key: str, value: float):
        async with self.db_session.begin():
            query = (
                update(Settings)
                .where(Settings.key == key)
                .values(value=value)
                .returning(Settings.value)
            )
            res = await self.db_session.execute(query)
            await self.db_session.commit()
            return res.scalar_one_or_none()

    async def set_param(self, key: str, value: float):
        async with self.db_session.begin():
            new_param = Settings(key=key, value=value)
            self.db_session.add(new_param)
            await self.db_session.commit()
            return value

    @cached(key_builder=lambda db_session, key: build_key(key))
    async def get_param(self, key: str):
        async with self.db_session.begin():
            query = select(Settings.value).where(Settings.key == key)
            res = await self.db_session.execute(query)
            return res.scalar_one_or_none()


class UserDAL(BaseDAL):
    async def add_user(self, user_id: int, username: str = None):
        async with self.db_session.begin():
            new_user = User(user_id=user_id, username=username)
            self.db_session.add(new_user)
            await self.db_session.commit()
            return new_user

    async def update_user(self, user_id: int, **kwargs):
        async with self.db_session.begin():
            query = (
                update(User)
                .where(User.user_id == user_id)
                .values(kwargs)
                .returning(User.user_id)
            )
            res = await self.db_session.execute(query)
            await self.db_session.commit()
            return res.scalar_one_or_none()

    async def user_exists(self, user_id: int) -> bool:
        async with self.db_session.begin():
            query = select(exists().where(User.user_id == user_id))
            res = await self.db_session.execute(query)
            return res.scalar()

    async def get_user(self, user_id: int) -> Union[User, None]:
        async with self.db_session.begin():
            query = select(User).where(User.user_id == user_id)
            res = await self.db_session.execute(query)
            return res.scalar()


class ReferralDAL(BaseDAL):
    async def add_referal(self, id_from: int, id_to: int):
        async with self.db_session.begin():
            new_referral = Referral(id_from=id_from, id_to=id_to)
            self.db_session.add(new_referral)
            await self.db_session.commit()
            return new_referral

    async def referral_exists(self, id_to: int):
        async with self.db_session.begin():
            query = select(exists().where(Referral.id_to == id_to))
            res = await self.db_session.execute(query)
            return res.scalar()

    @cached(key_builder=lambda db_session, id_from: build_key(id_from))
    async def get_refferals(self, id_from: int):
        async with self.db_session.begin():
            query = select(Referral.id_to).where(Referral.id_from == id_from)
            res = await self.db_session.execute(query)
            return res.scalars().all()


class OrderDAL(BaseDAL):
    async def add_order(self, user_id: int, **kwargs) -> Union[Order, None]:
        async with self.db_session.begin():
            order = Order(user_id=user_id, **kwargs)
            self.db_session.add(order)
            await self.db_session.commit()
            return order

    async def get_completed_orders_for_user(self, user_id: int):
        async with self.db_session.begin():
            query = (
                select(Order.price_rub)
                .where(Order.status == OrderStatus.COMPLETED, Order.user_id == user_id)
                .order_by(Order.id)
            )
            result = await self.db_session.execute(query)
            return result.scalars().all()

    async def get_orders_for_user(self, user_id: int):
        async with self.db_session.begin():
            query = select(Order).where(Order.user_id == user_id).order_by(Order.id)
            result = await self.db_session.execute(query)
            return result.scalars().all()

    async def get_completed_orders(self):
        async with self.db_session.begin():
            query = (
                select(Order)
                .where(Order.status == OrderStatus.COMPLETED)
                .order_by(Order.id)
            )
            result = await self.db_session.execute(query)
            return result.scalars().all()

    async def get_all_active_orders(self):
        async with self.db_session.begin():
            query = (
                select(Order)
                .where(Order.status != OrderStatus.COMPLETED)
                .order_by(Order.id)
            )
            result = await self.db_session.execute(query)
            return result.scalars().all()

    async def update_order(self, id: int, **kwargs):
        async with self.db_session.begin():
            query = update(Order).where(Order.id == id).values(kwargs).returning(Order)
            res = await self.db_session.execute(query)
            await self.db_session.commit()
            return res.scalar_one_or_none()

    async def delete_order(self, id: int):
        async with self.db_session.begin():
            query = delete(Order).where(Order.id == id)
            await self.db_session.execute(query)
            await self.db_session.commit()
            return id


class PromosDAL(BaseDAL):
    @cached(key_builder=lambda db_session: build_key("promo"))
    async def get_all_promos(self):
        async with self.db_session.begin():
            query = select(Promos).order_by(Promos.id)
            result = await self.db_session.execute(query)
            return result.scalars().all()

    async def add_promo(self, text: str):
        async with self.db_session.begin():
            new_promo = Promos(descriptions=text)
            self.db_session.add(new_promo)
            await self.db_session.commit()
            return new_promo

    async def delete_promo(self, id: int):
        async with self.db_session.begin():
            query = delete(Promos).where(Promos.id == id)
            await self.db_session.execute(query)
            await self.db_session.commit()
            return id
