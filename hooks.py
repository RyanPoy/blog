# /blog/hooks.py
from neotale.filters import FILTERS

# 从 neotale 包中导入你的 filter 函数
# 注意这里的路径是相对于项目根目录的
# from neotale.filters import date_format

# on_env 是 MkDocs 的一个 hook 函数。
# MkDocs 会在加载时自动寻找并执行这个名字的函数。
# 你不需要把它放在类里面。
def on_env(env, config, files):
    """
    在 Jinja 环境中注入自定义的 filter。
    """
    print("*"*50)
    print("HOOKS: Loading custom filter 'date_format' into Jinja environment.")
    print("*"*50)

    for name, fn in FILTERS.items():
        env.filters[name] = fn    
    
    return env
