from mkdocs.theme import BaseTheme
from mkdocs.utils import log
from .filters import FILTERS  # 从同级目录的 filters.py 导入你的函数

# 创建一个继承自 MkDocs BaseTheme 的新类
class NeotaleTheme(BaseTheme):
    """
    Neotale 主题，内置自定义 filters。
    """
    # 重写 extend_jinja_env 方法
    def extend_jinja_env(self, jinja_env):
        """
        在 Jinja2 环境中添加自定义的 filter。
        """
        # 'date_format' 是你在模板中使用的 filter 名称
        # date_format 是你从 filters.py 导入的 Python 函数
        for name, filter_fn in FILTERS.items():
            jinja_env.filters[name] = filter_fn
