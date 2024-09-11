import os
from dotenv import load_dotenv
from pdf2md import PDF2Markdown
from models.database import create_all

create_all()
load_dotenv()
api_key = os.getenv('API_KEY')

pdf2md = PDF2Markdown(
    pdf_path='./test/yh.pdf',
    model='qwen-vl-max-0809',
    api_key=api_key,
    base_url='https://dashscope.aliyuncs.com/compatible-mode/v1'
)

# 将第一页到第四页内容转为markdown
# markdown将保存在storage/markdown目录下
pdf2md.convert(1, 4)

# 重新识别第四页
pdf2md.convert(4, 4, True)
