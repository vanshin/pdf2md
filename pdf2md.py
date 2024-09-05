import datetime
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage

from util import encode_image, PDFSplitter, save_md

from model import RawPageContent


class BaseModel(object):

    sys_prompt = ''
    input_content = ''

    def __init__(self, model, api_key, base_url, max_retries=2, temperature=0):

        self.client = ChatOpenAI(
            model=model,
            temperature=temperature,
            api_key=api_key,
            base_url=base_url,
            max_retries=max_retries,
        )



class PDF2Image(BaseModel):

    sys_prompt = '''
    你需要帮助用户将上传的图片转为markdown格式。
    用户可能会输入当前图片内容的上文内容的markdown数据，如果用户给了上文，请根据已有的上文来转换当前上传的图片，注意保持文本格式的前后统一。
    最后返回的时候，请只返回上传的图片转换后的markdown内容，并且只返回markdown数据极可，例如:

    # 标题1
    ## 标题2
    this is a test content

    '''

    input_content = '''
    这是上文的内容：{pre}。
    请将图片的内容转为markdown。
    '''


    def __init__(self, pdf_path, model, api_key, base_url):

        super(PDF2Image, self).__init__(model, api_key, base_url)
        self.pdfer = PDFSplitter(pdf_path)


    def _convert(self, image_path, pre=''):
        """转换pdf图片为markdown"""

        # 图片处理
        base64_image = encode_image(image_path)
        url =  f"data:image/jpeg;base64,{base64_image}"

        # 准备消息
        messages = [
            SystemMessage(content=self.sys_prompt),
            HumanMessage(content=[
                {'type': 'text', 'text': self.input_content.format(pre=pre)},
                {'type': 'image_url', 'image_url': {'url': url}},
            ]),
        ]

        r = self.client.invoke(messages)

        # 处理可能的其他字符
        content = r.content
        if '```' in r.content:
            content = content.replace('```', '').replace('markdown', '')

        # 保存到数据库
        page = image_path.split('/')[-1].split('.')[0]
        RawPageContent.add({
            'name': self.pdfer.pdf_name,
            'page': int(page),
            'content': content,

        })
        return content

    def convert(self, start, end):

        convert_start = start
        pre_page_content = ''
        # 转换的时候需要取出前一页防止丢失文本格式
        if convert_start > 1:
            pre_page = RawPageContent.query_content_by_page(
                self.pdfer.pdf_name, convert_start-1)
            # 上一页从来没查询过
            if not pre_page:
                p = self.pdfer.convert_pdf(convert_start-1, convert_start-1)
                pre_page_content = self._convert(p[0])
            #
            else:
                pre_page_content = pre_page.content

        image_path_list = self.pdfer.convert_pdf(start, end)

        for p in image_path_list:
            pre_page_content = self._convert(p, pre_page_content)
        pages = list(range(start, end+1))
        contents = RawPageContent.query_contents_by_pages(
            self.pdfer.pdf_name, pages
        )

        md = ''.join([c.content for c in contents])
        now = datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
        name = f'{self.pdfer.pdf_name}_{now}_{start}-{end}.md'
        save_md(name, md)

