import os
from sqlalchemy import create_engine
from dotenv import load_dotenv
from urllib.parse import quote_plus as urlquote

from util import HOME
from models import Base


def fmt_mysql():
    """从环境变量中读取数据库连接信息"""

    db_user = os.getenv('DB_USERNAME')
    db_password = os.getenv('DB_PASSWORD')
    host = os.getenv('DB_HOST')
    port = os.getenv('DB_PORT')
    db = os.getenv('DB_DATABASE')
    pw = urlquote(db_password)
    conn_str = f"mysql+pymysql://{db_user}:{pw}@{host}:{port}/{db}"
    return conn_str


def fmt_sqlite():
    """sqlite设置本地路径"""

    db_path = os.path.join(HOME, 'storage', 'db')
    db_name_path = os.path.join(db_path, 'pdf2md.db')
    if not os.path.exists(db_path):
        os.makedirs(db_path)
    return f"sqlite:///{db_name_path}"


def make_engine():

    engine_str = 'sqlite'
    db_type = os.getenv('DB_TYPE')
    if db_type == 'sqlite':
        engine_str = fmt_sqlite()
    elif db_type == 'fmt_mysql':
        engine_str = fmt_mysql()
    else:
        raise Exception('invalid db type')

    return create_engine(engine_str)


load_dotenv()
engine = make_engine()


def create_all():
    from models.api import APIKey
    from models.pdf import PDFFile
    from models.markdown import PDFMarkdown
    Base.metadata.create_all(engine)
