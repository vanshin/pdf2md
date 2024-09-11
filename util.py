import os
import time
import base64
from functools import wraps
from dotenv import load_dotenv

load_dotenv()
debug = os.getenv('DEBUG')
HOME = os.path.dirname(os.path.abspath(__file__))


def time_it(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        if debug:
            print(f"执行 {func.__name__} 耗时 {end_time - start_time:.8f} 秒")
        return result
    return wrapper


def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')


def save_md(name, md_str):

    md_path = os.path.join(HOME, 'storage', 'markdown')
    if not os.path.exists(md_path):
        os.makedirs(md_path)

    md_name = os.path.join(md_path, name)
    with open(md_name, "w") as f:
        f.write(md_str)
