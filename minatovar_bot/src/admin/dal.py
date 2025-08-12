from sqlalchemy import delete, exists, select, update
from src.admin.models import AdminUser, Promos, Settings
from src.cache.redis import build_key, cached
from src.db.dals import BaseDAL


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


class AdminDAL(BaseDAL):
    async def get_admin_by_username(self, username: str) -> AdminUser | None:
        async with self.db_session.begin():
            query = select(AdminUser).where(AdminUser.username == username)
            res = await self.db_session.execute(query)
            return res.scalar_one_or_none()
    
    async def get_all_admins(self) -> list[AdminUser]:
        async with self.db_session.begin():
            query = select(AdminUser)
            res = await self.db_session.execute(query)
            return res.scalars().all()
    
    async def create_admin(self, username: str, hashed_password: str) -> AdminUser:
        async with self.db_session.begin():
            admin = AdminUser(username=username, hashed_password=hashed_password)
            self.db_session.add(admin)
            await self.db_session.commit()
            return admin
