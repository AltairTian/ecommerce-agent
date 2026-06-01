"""检索器模块 —— 将用户查询转为向量，从 ChromaDB 检索最相关文档。"""

import logging

from config.settings import RAG_TOP_K
from src.rag.embeddings import embed_query
from src.rag.vector_store import search_similar, get_store_count

logger = logging.getLogger("rag")


def retrieve(query: str, top_k: int | None = None) -> list[dict]:
    """根据用户查询检索最相关的知识库文档块。

    Args:
        query: 用户问题或检索查询。
        top_k: 返回结果数，默认 RAG_TOP_K。

    Returns:
        相关文档块列表，每项包含 id、document、metadata、distance。
    """
    if top_k is None:
        top_k = RAG_TOP_K

    store_count = get_store_count()
    if store_count == 0:
        logger.warning("Retrieval skipped: vector store is empty")
        return []

    query_embedding = embed_query(query)
    results = search_similar(query_embedding, top_k=top_k)

    logger.info(
        "Retrieved %d results for query: '%s'",
        len(results),
        query[:80],
    )
    return results


def retrieve_as_context(query: str, top_k: int | None = None) -> str:
    """检索并拼接为上下文文本，可直接注入 Agent 的 system prompt。

    Args:
        query: 用户问题。
        top_k: 检索数量。

    Returns:
        拼接好的上下文字符串，格式为 "### 相关知识 1\n...\n### 相关知识 2\n..."
    """
    results = retrieve(query, top_k=top_k)

    if not results:
        return ""

    blocks = []
    for i, r in enumerate(results, 1):
        source = r.get("metadata", {}).get("source", "unknown")
        heading = r.get("metadata", {}).get("heading", "")
        header = f"### 相关知识 {i}"
        if heading:
            header += f"：{heading}"
        header += f"（来源：{source}）"
        blocks.append(f"{header}\n{r['document']}")

    return "\n\n".join(blocks)
