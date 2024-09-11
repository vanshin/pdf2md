import datetime
from sqlalchemy import DateTime
from sqlalchemy.inspection import inspect
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):

    __abstract__ = True

    id: Mapped[int] = mapped_column(primary_key=True)
    ctime: Mapped[datetime.datetime] = mapped_column(
        DateTime, default=datetime.datetime.utcnow
    )
    utime: Mapped[datetime.datetime] = mapped_column(
        DateTime, default=datetime.datetime.utcnow,
        onupdate=datetime.datetime.utcnow
    )

    def __repr__(self):
        columns = inspect(self).mapper.column_attrs
        column_values = {col.key: getattr(self, col.key) for col in columns}
        return f"<{self.__class__.__name__}({column_values})>"
