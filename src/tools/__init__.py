"""统一导出所有 LangChain tools。"""


def _get_tools():
    """惰性导入 tools 列表 —— 避免导入 metrics 时就强制依赖 langchain。"""
    from src.tools.langchain_tools import tools
    return tools


def __getattr__(name):
    """支持 `from src.tools import tools` 的惰性导入。"""
    if name == "tools":
        return _get_tools()
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")

__all__ = ["tools"]
