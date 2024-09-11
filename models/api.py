from models import Base
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column


class APIKey(Base):
    """用来管理大模型的api和key"""

    __tablename__ = "api_key"

    name: Mapped[str] = mapped_column(String(200), comment='自定义的key名称')
    api_key: Mapped[str] = mapped_column(String(200), comment='apikey')
    base_url: Mapped[str] = mapped_column(String(200), comment='模型连接url')
    default_model: Mapped[str] = mapped_column(
        String(200), default='', comment='默认使用的模型'
    )
