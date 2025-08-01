from sqlalchemy import delete, select, update
from src.db.dals import BaseDAL
from src.orders.models import Order, OrderStatus


class OrderDAL(BaseDAL):
    async def add_order(self, user_id: int, **kwargs) -> Order | None:
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

