class BaseError(Exception):

    def __init__(self, msg='', code='1000', data=None):
        self.msg = msg
        self.code = getattr(self, 'code', code)
        self.data = data

    def __str__(self):
        return '[code:%s] msg:%s' % (self.code, self.msg)


class LLMError(BaseError):
    code = '1001'


class DataError(BaseError):
    code = '1002'


class ParamError(BaseError):
    code = '1003'
