from sqlalchemy import select, update, delete
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError

from models.database import engine


class BaseRepository:
    """基础仓库类"""

    def __init__(self, model_class, session=None):
        self.model_class = model_class
        self.session_owned = True
        self.session = session or self._create_session()

    def _create_session(self):
        # 这里可以配置 sessionmaker 或使用已配置的全局 sessionmaker
        SessionLocal = sessionmaker(bind=engine)
        self.session_owned = False
        ses = SessionLocal()
        return ses

    def add(self, instance):
        try:
            self.session.add(instance)
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            raise e
        finally:
            # 只有自己创建的session才可以关闭
            if self.session_owned:
                self.session.close()

    def get_by_id(self, id):
        return self.session.query(self.model_class).get(id)

    def get_by(self, col, value):
        col_name = getattr(self.model_class, col)
        if not col_name:
            raise SQLAlchemyError(f'not found column {col}')
        s = select(self.model_class).where(col_name == value)
        r = self.session.execute(s).first()
        return r[0] if r else None

    def modify(self, instance):
        try:
            self.session.commit()
            return instance
        except SQLAlchemyError as e:
            self.session.rollback()
            raise e
        finally:
            if self.session_owned:
                self.session.close()

    def delete(self, id):
        try:
            instance = self.get_by_id(id)
            if instance:
                self.session.delete(instance)
                self.session.commit()
                return True
            return False
        except SQLAlchemyError as e:
            self.session.rollback()
            raise e
        finally:
            if self.session_owned:
                self.session.close()

    def list_all(self):
        try:
            return self.session.query(self.model_class).all()
        except SQLAlchemyError as e:
            raise e
        finally:
            if self.session_owned:
                self.session.close()
