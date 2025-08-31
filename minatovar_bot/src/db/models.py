from datetime import datetime
from sqlalchemy import BIGINT, DateTime, MetaData, func
from sqlalchemy.orm import declarative_base, Mapped, mapped_column

POSTGRES_INDEXES_NAMING_CONVENTION = {
    "ix": "%(column_0_label)s_idx",
    "uq": "%(table_name)s_%(column_0_name)s_key",
    "ck": "%(table_name)s_%(constraint_name)s_check",
    "fk": "%(table_name)s_%(column_0_name)s_fkey",
    "pk": "%(table_name)s_pkey",
}

Base = declarative_base(
    metadata=MetaData(naming_convention=POSTGRES_INDEXES_NAMING_CONVENTION)
)


class BaseModel(Base):
    __abstract__ = True

    id: Mapped[int] = mapped_column(BIGINT, primary_key=True)
    time_created: Mapped[datetime] = mapped_column(DateTime(), server_default=func.now())
    time_updated: Mapped[datetime] = mapped_column(DateTime(), server_default=func.now(), onupdate=func.now())
