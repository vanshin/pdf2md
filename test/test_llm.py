import os
import sys
import pytest

TEST_DIR = os.path.dirname(os.path.abspath(__file__))
HOME = os.path.dirname(TEST_DIR)
sys.path.append(HOME)

from pdf2img import PDF2Img
from llm import PDF2MarkdownLLM, MergeLLM
from util import encode_image
from repositories.markdown import PDFMarkdownRepo


class TestLLM(object):

    @pytest.fixture(autouse=True)
    def setup(self):
        PDF2MarkdownLLM.save_key(
            'qwen',
            'https://dashscope.aliyuncs.com/compatible-mode/v1',
            'sk-2d09788c60164aa0a53e6a5ec4cbb8b5',
            'qwen-vl-max-0809'
        )
        PDF2MarkdownLLM.save_key(
            'deepseek',
            'https://api.deepseek.com',
            'sk-0d9f4d93c5894fceaaba2fd87ae27ff1',
            'deepseek-chat'
        )
        self.llm = PDF2MarkdownLLM.from_name('qwen')
        # self.mgllm = MergeLLM.from_name('deepseek')
        self.mgllm = MergeLLM.from_name('qwen')
        self.p2i = PDF2Img(os.path.join(TEST_DIR, 'yh.pdf'))

    def test_invoke(self):
        self.p2i.convert_pdf(1, 5)
        base64_image = encode_image(
            '/home/vanshin/pdf2md/storage/pdf_image/yh/4.png'
        )
        r = self.llm.invoke(base64_image, '')
        assert '83962802' in r

    def test_invoke_with_previous(self):
        page_4_content = PDFMarkdownRepo().query_content_by_page(
            self.p2i.pdf_id, 4)
        base64_image = encode_image(
            '/home/vanshin/pdf2md/storage/pdf_image/yh/5.png'
        )
        r = self.llm.invoke(base64_image, page_4_content.content)
        assert r != ''
