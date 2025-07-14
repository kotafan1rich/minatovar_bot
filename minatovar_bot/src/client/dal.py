from sqlalchemy import exists, select, update
from src.cache.redis import build_key, cached
from src.client.models import User
from src.db.dals import BaseDAL
from src.orders.models import Referral


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

    async def get_user(self, user_id: int) -> User | None:
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
