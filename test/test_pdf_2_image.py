import os
import sys
import pytest

TEST_DIR = os.path.dirname(os.path.abspath(__file__))
HOME = os.path.dirname(TEST_DIR)
sys.path.append(HOME)

from pdf2md import PDF2Image
from model import RawPageContent



class TestPDF(object):

    @pytest.fixture(autouse=True)
    def setup(self):
        self.pi = PDF2Image(
            '/home/vanshin/pdf2md/test/yh.pdf',
            'qwen-vl-max-0809',
            'sk-c75c035163d54342babc6813106a8140',
            'https://dashscope.aliyuncs.com/compatible-mode/v1'
        )

    def test_convert_part(self):

        RawPageContent.clear(self.pi.pdfer.pdf_name)
        self.pi.convert(10, 11)
        r = RawPageContent.query_contents_by_pages(
            self.pi.pdfer.pdf_name, list(range(10, 12))
        )
        print(r)
        assert len(r) == 2




if __name__ == '__main__':
    testps = TestPDFSplitter()
    testps.test_pdf_info()
