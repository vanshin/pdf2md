from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import AIMessage

from models.api import APIKey
from repositories.api import APIKeyRepo
from exception import DataError
from prompts import (
    PDF2MD_SYS, PDF2MD_USER,
    MERGE_MD_SYS, MERGE_MD_USER
)


class BaseLLM(object):

    def __init__(self, model, api_key, base_url, max_retries=2, temperature=0):

        self.client = ChatOpenAI(
            model=model,
            temperature=temperature,
            api_key=api_key,
            base_url=base_url,
            max_retries=max_retries,
        )
        self.setup()

    def setup(self):
        pass

    @classmethod
    def from_name(cls, name, model_name=None):
        """从key的名字直接实例化"""
        api_key = APIKeyRepo().get_by_name(name)
        if not api_key:
            raise DataError('API key不存在')
        model_name = model_name or api_key.default_model
        return cls(
            model_name,
            api_key.api_key,
            api_key.base_url
        )

    @staticmethod
    def save_key(name, base_url, api_key, default_model):
        """添加新的key"""
        ak = APIKey(
            name=name, base_url=base_url,
            api_key=api_key, default_model=default_model

        )
        APIKeyRepo().add(ak)


class PDF2MarkdownLLM(BaseLLM):
    '''

    请注意需要将原始数据全部保留下来，不可省略，无法使用markdown表示的格式，请使用纯文本保留数据，
    '''

    def setup(self):
        """设置prompt和解析器"""

        user = [
            {'type': 'text', 'text': PDF2MD_USER},
            {
                'type': 'image_url',
                'image_url': {'url': 'data:image/jpeg;base64,{image_data}'}
            },
        ]

        t = ChatPromptTemplate.from_messages([
            ('system', PDF2MD_SYS),
            ('user', user),
        ])

        self.client = t | self.client | self.parse

    def parse(self, output: AIMessage):
        content = output.content
        if '```' in content:
            content = content.replace('```', '').replace('markdown', '')
        return content

    def invoke(self, image_data, previous=''):
        return self.client.invoke({
            'image_data': image_data, 'previous': previous
        })


class MergeLLM(BaseLLM):

    def setup(self):
        """设置prompt和解析器"""

        t = ChatPromptTemplate.from_messages([
            ('user', MERGE_MD_USER),
            ('system', MERGE_MD_SYS),
        ])

        self.client = t | self.client | self.parse

    def parse(self, output: AIMessage):
        content = output.content
        if '```' in content:
            content = content.replace('```', '').replace('markdown', '')
        return content

    def invoke(self, one, two):
        return self.client.invoke({'one': one, 'two': two})
