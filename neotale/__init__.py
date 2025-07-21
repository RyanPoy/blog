from mkdocs.themes import Theme
from mkdocs.utils import log

class NeotaleTheme(Theme):
    def __init__(self):
        super().__init__(name='neotale', static_templates=['404.html'])
        # 添加其他主题初始化配置
        print("*"*50)

    def get_env(self):
        # 获取父类的Jinja环境
        env = super().get_env()
        
        # 动态导入自定义过滤器
        try:
            from .filters import date_format
            env.filters['date_format'] = date_format
            log.debug("Successfully loaded neotale date_format filter")
        except ImportError as e:
            log.error(f"Failed to load neotale filters: {e}")
        
        return env
