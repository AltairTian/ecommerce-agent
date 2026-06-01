"""嵌入模型模块 —— 文本向量化的唯一入口。

使用 Sentence-Transformers 将文本转为稠密向量，供 ChromaDB 存储和检索。
"""

from __future__ import annotations

import logging
from typing import List

from sentence_transformers import SentenceTransformer

from config.settings import EMBEDDING_MODEL

logger = logging.getLogger("rag")

# 模块级单例，首次使用时加载
_embedding_model: SentenceTransformer | None = None


def _get_model() -> SentenceTransformer:
    """惰性加载嵌入模型（首次调用时下载/加载到内存）。"""
    global _embedding_model
    if _embedding_model is None:
        logger.info("Loading embedding model: %s", EMBEDDING_MODEL)
        _embedding_model = SentenceTransformer(EMBEDDING_MODEL)
        logger.info("Embedding model loaded, dim=%d", _embedding_model.get_embedding_dimension())
    return _embedding_model


def embed_texts(texts: List[str]) -> List[List[float]]:
    """将文本列表转为向量列表。

    Args:
        texts: 待编码的文本列表，每个元素是一段独立文本。

    Returns:
        等长的向量列表，每个向量是 float 列表。
    """
    if not texts:
        return []
    model = _get_model()
    embeddings = model.encode(texts, normalize_embeddings=True)
    return embeddings.tolist()


def embed_query(query: str) -> List[float]:
    """将单条查询文本转为向量。

    Args:
        query: 用户查询字符串。

    Returns:
        查询向量（float 列表）。
    """
    result = embed_texts([query])
    return result[0]
