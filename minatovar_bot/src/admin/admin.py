from typing import Any, Dict, Union

import anyio
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session
from src.admin.models import AdminUser, Promos, Settings
from src.auth.utils import get_hash
from src.db.admin import AdminBase
from starlette.requests import Request


class SettingsAdmin(AdminBase):
    model = Settings

    fields = [model.key, model.value, model.time_updated]


class PromoAdmin(AdminBase):
    model = Promos

    fields = [model.id, model.descriptions, model.time_updated]


class AdminsAdmin(AdminBase):
    model = AdminUser

    fields = [
        model.id,
        model.username,
        model.user,
        model.hashed_password,
        model.time_updated,
        model.time_created,
    ]

    exclude_fields_from_edit = [
        model.id,
        model.hashed_password,
        model.time_created,
        model.time_updated,
    ]

    async def create(self, request: Request, data: Dict[str, Any]) -> Any:
        try:
            data["hashed_password"] = get_hash(data["hashed_password"])
            data = await self._arrange_data(request, data)
            await self.validate(request, data)
            session: Union[Session, AsyncSession] = request.state.session
            obj = await self._populate_obj(request, self.model(), data)
            session.add(obj)
            await self.before_create(request, data, obj)
            if isinstance(session, AsyncSession):
                await session.commit()
                await session.refresh(obj)
            else:
                await anyio.to_thread.run_sync(session.commit)  # type: ignore[arg-type]
                await anyio.to_thread.run_sync(session.refresh, obj)  # type: ignore[arg-type]
            await self.after_create(request, obj)
            return obj
        except Exception as e:
            return self.handle_exception(e)

    async def edit(self, request: Request, pk: Any, data: Dict[str, Any]) -> Any:
        try:
            password = data.get("hashed_password")
            if password:
                data["hashed_password"] = get_hash(password)
            data = await self._arrange_data(request, data, True)
            await self.validate(request, data)
            session: Union[Session, AsyncSession] = request.state.session
            obj = await self.find_by_pk(request, pk)
            await self._populate_obj(request, obj, data, True)
            session.add(obj)
            await self.before_edit(request, data, obj)
            if isinstance(session, AsyncSession):
                await session.commit()
                await session.refresh(obj)
            else:
                await anyio.to_thread.run_sync(session.commit)  # type: ignore[arg-type]
                await anyio.to_thread.run_sync(session.refresh, obj)  # type: ignore[arg-type]
            await self.after_edit(request, obj)
            return obj
        except Exception as e:
            self.handle_exception(e)
