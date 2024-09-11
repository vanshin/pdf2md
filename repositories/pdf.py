from repositories.base import BaseRepository
from models.pdf import PDFFile


class PDFFileRepo(BaseRepository):

    def __init__(self, session=None):
        super().__init__(PDFFile, session)
