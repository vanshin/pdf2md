PDF2MD_SYS = '''
    你需要帮助用户将上传的图片内容识别并提取后转为markdown格式。
    ---以下是文档的背景信息---
    用户上传的图片是pdf文档中的一页，在<previous>标签包裹的是图片的上一页内容，格式是markdown。
    ---图片内容转换注意事项---
    请先了解previous标签中的markdown内容，了解其文档结构，包括标题，表格，列表等markdown格式
    任何图片中的内容都需要保留，无法处理的的内容就使用纯文本保留
    ---返回数据格式---
    只返回上传的图片转换后的markdown内容，不要携带任何previous标签的数据。并且只返回markdown数据，例如:

    ```markdown
    this is a test content
    # 标题1
    ## 标题2
    this is a test content
    ```

    '''


PDF2MD_USER = '''
    <previous>{previous}<previous>
    请根据上文previous标签内容将图片的内容转为markdown格式。
'''


MERGE_MD_SYS = '''
你需要根据我提供的markdown文档上文内容来修复markdown文档的下文内容，包括适当的标题层级、列表、表格格式以及任何格式化细节（如加粗或斜体文字）。
请保证修复的文档在内容上没有丢失和改变，并且不要添加新的内容
请返回修复后的下文markdown文档，如果因为上下文内容切分导致不能满足markdown格式请处理成纯文本
'''

MERGE_MD_USER = '''
请帮我修复下文文本
以下上文文本
{one}
------------
以下是需要修复的下文文本
{two}

请按照markdown格式返回下文文本，并保持文本内容和原来一致

'''
