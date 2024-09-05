from typing import List
from typing import Optional
from sqlalchemy import ForeignKey
from sqlalchemy import Integer, String
from sqlalchemy import create_engine
from sqlalchemy import select, update, delete
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.schema import UniqueConstraint
from urllib.parse import quote_plus as urlquote


class Base(DeclarativeBase):
    pass


class RawPageContent(Base):
    __tablename__ = "raw_content"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(200))
    page: Mapped[int] = mapped_column(Integer)
    content: Mapped[str] = mapped_column(String(16000))

    __table_args__ = (
        UniqueConstraint('name', 'page', name='uq_name_page', ),
    )

    def __repr__(self) -> str:
        return f"raw_content(id={self.id!r}, name={self.name!r}, page={self.page!r})"

    @classmethod
    def add(cls, data: dict):
        if 'name' not in data:
            raise Exception('name 不存在')
        if 'page' not in data:
            raise Exception('page 不存在')

        s = select(cls.id).where(cls.name==data['name'], cls.page==data['page'])

        with Session(engine) as session:

            r = session.execute(s).all()
            if r:
                u = update(cls).where(
                    cls.name==data['name'],
                    cls.page==data['page']
                ).values(content=data['content'])
                session.execute(u)
            else:
                u = cls(**data)
                session.add(u)
            session.commit()

    @classmethod
    def query_content_by_page(cls, name, page):
        s = select(cls).where(cls.page==page, cls.name==name)

        with Session(engine) as session:
            r = session.execute(s).first()
        return r[0] if r else {}

    @classmethod
    def query_contents_by_pages(cls, name, pages):
        s = select(cls.content, cls.name, cls.page, cls.id).where(
            cls.page.in_(pages), cls.name==name
        ).order_by(cls.page)

        with Session(engine) as session:
            r = session.execute(s).all()
        return r

    @classmethod
    def clear(cls, name):
        with Session(engine) as session:
            d = delete(cls).where(cls.name==name)
            session.execute(d)
            session.commit()

engine = create_engine(f"mysql+pymysql://jianjin:{urlquote('sql@jianjin')}@172.16.1.112:3306/rag_chat", echo=True)

Base.metadata.create_all(engine)


r = RawPageContent.query_contents_by_pages('yh', [9, 10])
print(r[0].content)
