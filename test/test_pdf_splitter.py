import os
import sys

TEST_DIR = os.path.dirname(os.path.abspath(__file__))
HOME = os.path.dirname(TEST_DIR)
sys.path.append(HOME)

from util import PDFSplitter


class TestPDFSplitter(object):

    @property
    def ps(self):
        pdf_path = os.path.join(TEST_DIR, 'yh.pdf')
        return PDFSplitter(pdf_path)


    def test_init(self):
        self.ps.delete_images()
        assert self.ps.pdf_name == 'yh'

    def test_pdf_info(self):
        info = self.ps.pdf_info()
        assert info['pages'] == 283

    def test_convert_pdf_to_image(self):
        """这个方法每次都重新生成图片"""
        res = self.ps.convert_pdf_to_image(10, 20)
        assert len(res) == 11
        assert res[0].endswith('10.png')
        assert res[-1].endswith('20.png')

    def test_exist_pdf_images(self):
        exists = self.ps.exist_pdf_images()
        assert len(exists) == 11

    def test_rest_image_range(self):
        res = self.ps.rest_image_range(8, 20)
        print(res)
        assert res[0] == [(8, 9)]
        assert res[1] == list(range(10, 21))

    def test_rest_image_range_same(self):
        res = self.ps.rest_image_range(10, 10)
        print(res)
        assert res[0] == []
        assert res[1] == [10]

    def test_delete_images(self):
        self.ps.delete_images()
        exists = self.ps.exist_pdf_images()
        assert len(exists) == 0
        assert self.ps.rest_image_range() == ([(1, self.ps.pdf_info()['pages'])], [])

    def test_convert_pdf(self):
        self.test_convert_pdf_to_image()
        res = self.ps.convert_pdf(8, 20)
        assert len(res) == 13
        res = [i[-6:] for i in res]
        assert '/8.png' in res
        assert '20.png' in res



if __name__ == '__main__':
    testps = TestPDFSplitter()
    testps.test_pdf_info()
