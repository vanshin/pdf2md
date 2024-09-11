from sqlalchemy import select, update, delete, insert
from repositories.base import BaseRepository
from models.markdown import PDFMarkdown
from exception import ParamError


class PDFMarkdownRepo(BaseRepository):

    def __init__(self, session=None):
        super().__init__(PDFMarkdown, session)

    def add_or_update(self, md: PDFMarkdown):
        """添加或者更新"""

        if not md.pdf_id:
            raise ParamError('pdf_id不存在')
        if not md.page:
            raise ParamError('page不存在')

        s = select(self.model_class.id).where(
            self.model_class.pdf_id == md.pdf_id,
            self.model_class.page == md.page
        )

        r = self.session.execute(s).all()
        if r:
            u = update(self.model_class).where(
                self.model_class.pdf_id == md.pdf_id,
                self.model_class.page == md.page,
            ).values(content=md.content)
            self.session.execute(u)
        else:
            self.session.add(md)
        self.session.commit()

    def query_content_by_page(self, pdf_id, page):
        s = select(self.model_class).where(
            self.model_class.page == page,
            self.model_class.pdf_id == pdf_id
        )

        r = self.session.execute(s).first()
        return r[0] if r else {}

    def query_contents_by_pages(self, pdf_id, pages):
        s = select(
            self.model_class.content,
            self.model_class.pdf_id,
            self.model_class.page,
            self.model_class.id
        ).where(
            self.model_class.page.in_(pages),
            self.model_class.pdf_id == pdf_id
        ).order_by(self.model_class.page)

        r = self.session.execute(s).all()
        return r

    def clear(self, pdf_id):
        d = delete(self.model_class).where(
                self.model_class.pdf_id == pdf_id)
        self.session.execute(d)
        self.session.commit()
