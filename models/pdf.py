from sqlalchemy import DateTime, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column
from models import Base


class PDFFile(Base):
    __tablename__ = "pdf_file"

    pdf_name: Mapped[str] = mapped_column(String(200), comment='pdf文件的名字')
    pdf_page_count: Mapped[int] = mapped_column(Integer, comment='pdf文件总页数')
