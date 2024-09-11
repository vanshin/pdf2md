import datetime

from llm import PDF2MarkdownLLM
from pdf2img import PDF2Img
from models.markdown import PDFMarkdown
from repositories.markdown import PDFMarkdownRepo
from util import encode_image, save_md, time_it


class PDF2Markdown(object):

    def __init__(self, pdf_path, model, api_key, base_url):

        self.pdfer = PDF2Img(pdf_path)
        self.llm = PDF2MarkdownLLM(model, api_key, base_url)

    @time_it
    def _convert(self, image_path, previous='', re_convert=False):
        """转换pdf图片为markdown"""

        pdf_md_repo = PDFMarkdownRepo()
        page = image_path.split('/')[-1].split('.')[0]

        # 已经生成过则直接返回
        content = pdf_md_repo.query_content_by_page(
            self.pdfer.pdf_id, page
        )
        if not re_convert and content:
            return content

        # 图片处理
        base64_image = encode_image(image_path)

        # 调用大模型
        r = self.llm.invoke(base64_image, previous)

        # 保存到数据库
        md = PDFMarkdown(
            pdf_id=self.pdfer.pdf_id,
            page=int(page),
            content=r,
        )
        pdf_md_repo.add_or_update(md)

        return r

    def convert(self, start, end, re_convert=False):

        pdfmd_repo = PDFMarkdownRepo()

        convert_start = start
        pre_page_content = ''

        # 转换的时候需要取出前一页防止丢失文本格式
        if convert_start > 1:
            pre_page = pdfmd_repo.query_content_by_page(
                self.pdfer.pdf_id, convert_start-1)

            # 没有上一页则转换
            if not pre_page:
                p = self.pdfer.convert_pdf(convert_start-1, convert_start-1)
                pre_page_content = self._convert(p[0])
            else:
                pre_page_content = pre_page.content

        image_path_list = self.pdfer.convert_pdf(start, end)
        for p in image_path_list:
            pre_page_content = self._convert(p, pre_page_content, re_convert)

        pages = list(range(start, end+1))
        contents = pdfmd_repo.query_contents_by_pages(
            self.pdfer.pdf_id, pages
        )

        md = ''.join([c.content for c in contents])
        now = datetime.datetime.now().strftime('%Y-%m-%dT%H%M%S')
        name = f'{self.pdfer.pdf_name}_{now}_Page{start}-{end}.md'
        save_md(name, md)
