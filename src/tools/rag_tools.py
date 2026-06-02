"""RAG 检索工具 —— 将知识库检索包装为 Agent 可调用的纯函数。

Agent 可以调用 search_knowledge_base 来查询电商领域知识。
"""

from src.rag.retriever import retrieve, retrieve_as_context


def search_knowledge_base(query: str, top_k: int = 3) -> str:
    """在电商知识库中搜索与查询相关的文档。

    当用户询问指标定义、业务规则、分析方法论等知识性问题时使用此函数。
    不要在查询数据库指标（GMV、订单量等）时使用——那些有专门的工具。

    Args:
        query: 搜索查询，尽量用关键词而非完整句子。
        top_k: 返回结果数，默认 3。

    Returns:
        格式化的相关文档内容，或空字符串（知识库为空时）。
    """
    return retrieve_as_context(query, top_k=top_k)
