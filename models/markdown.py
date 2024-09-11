from models import Base
from sqlalchemy import String, Integer, Text
from sqlalchemy.schema import UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column


class PDFMarkdown(Base):

    __tablename__ = "pdf_markdown"
    __table_args__ = (
        UniqueConstraint('pdf_id', 'page', name='uq_pdf_id_page', ),
        {'comment': 'pdf转换以后的markdown'},
    )

    pdf_id: Mapped[int] = mapped_column(Integer, comment='pdf文件ID')
    page: Mapped[int] = mapped_column(Integer, comment='所在页')
    content: Mapped[str] = mapped_column(Text, comment='当前页的markdown内容')


class MarkdownSegment(Base):
    __tablename__ = "markdown_segment"
    __table_args__ = (
        {'comment': 'pdf内容经过处理后的分片'},
    )

    markdown_id: Mapped[int] = mapped_column(Integer, comment='markdown文件ID')
    level_one: Mapped[str] = mapped_column(String(200), comment='当前内容所在一级标题')
    level_two: Mapped[str] = mapped_column(String(200), comment='当前页所在二级标题')
    level_three: Mapped[str] = mapped_column(String(200), comment='当前页所三级标题')
    summary: Mapped[str] = mapped_column(Text, comment='当前页内容汇总')
    content: Mapped[str] = mapped_column(Text)
