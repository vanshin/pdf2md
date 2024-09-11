import os
import sys
import pytest

TEST_DIR = os.path.dirname(os.path.abspath(__file__))
HOME = os.path.dirname(TEST_DIR)
sys.path.append(HOME)


from pdf2md import PDF2Markdown
from repositories.markdown import PDFMarkdownRepo


class TestPDF(object):

    @pytest.fixture(autouse=True)
    def setup(self):
        self.p2m = PDF2Markdown(
            '/home/vanshin/pdf2md/test/yh.pdf',
            'qwen-vl-max-0809',
            'sk-2d09788c60164aa0a53e6a5ec4cbb8b5',
            'https://dashscope.aliyuncs.com/compatible-mode/v1'
        )

    def test_convert_part(self):

        PDFMarkdownRepo().clear(self.p2m.pdfer.pdf_id)
        self.p2m.convert(10, 11)
        r = PDFMarkdownRepo().query_contents_by_pages(
            self.p2m.pdfer.pdf_id, list(range(10, 12))
        )
        print(r)
        assert len(r) == 2


