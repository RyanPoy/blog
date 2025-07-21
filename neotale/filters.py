from datetime import datetime
import re

def format_date(self, date_str, format="%B %d, %Y"):
    """格式化日期字符串"""
    dt = None
    try:
        dt = datetime.strptime(date_str, "%Y-%m-%d")
    except (TypeError, ValueError):
        try:
            dt = datetime.strptime(date_str, "%Y/%m/%d")
        except:
            dt = None
    if dt:
        return dt.strftime(format)
    return date_str
    

def markdown_summary(self, text, length=200):
    """从Markdown生成纯文本摘要"""
    clean_text = re.sub(r'!?\[(.*?)\]\(.*?\)', r'\1', text)
    clean_text = re.sub(r'[#*_~`]', '', clean_text)
    clean_text = re.sub(r'\n+', ' ', clean_text).strip()
    return clean_text[:length] + "..." if len(clean_text) > length else clean_text

def human_size(self, size_bytes):
    """将字节数转换为人类可读的大小"""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.1f} PB"

FILTERS = {
    'format_date': format_date,
    'markdown_summary': markdown_summary,
    'human_size': human_size,
}