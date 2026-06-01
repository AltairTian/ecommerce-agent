"""向量数据库模块 —— ChromaDB 连接与 collection 管理。

提供持久化的向量存储，支持文档添加和相似度检索。
"""

from __future__ import annotations

import logging
from typing import List

import chromadb
from chromadb.config import Settings as ChromaSettings

from config.settings import VECTOR_DB_PATH, RAG_TOP_K

logger = logging.getLogger("rag")

COLLECTION_NAME = "ecommerce_knowledge"

# 模块级单例
_client: chromadb.PersistentClient | None = None
_collection: chromadb.Collection | None = None


def _get_client() -> chromadb.PersistentClient:
    """获取 ChromaDB 持久化客户端。"""
    global _client
    if _client is None:
        VECTOR_DB_PATH.mkdir(parents=True, exist_ok=True)
        logger.info("Connecting to ChromaDB at %s", VECTOR_DB_PATH)
        _client = chromadb.PersistentClient(
            path=str(VECTOR_DB_PATH),
            settings=ChromaSettings(anonymized_telemetry=False),
        )
    return _client


def get_collection() -> chromadb.Collection:
    """获取或创建知识库 collection。"""
    global _collection
    if _collection is None:
        client = _get_client()
        _collection = client.get_or_create_collection(
            name=COLLECTION_NAME,
            metadata={"description": "电商知识库"},
        )
        logger.info("Collection '%s' ready, count=%d", COLLECTION_NAME, _collection.count())
    return _collection


def add_to_store(
    ids: List[str],
    documents: List[str],
    embeddings: List[List[float]],
    metadatas: List[dict] | None = None,
) -> None:
    """批量添加文档到向量存储。

    Args:
        ids: 文档块唯一 ID（如 "ecommerce_metrics.md_chunk_0"）。
        documents: 文档块原始文本。
        embeddings: 文档块对应的向量。
        metadatas: 元数据（如 {"source": "file.md", "chunk_index": 0}）。
    """
    if not ids:
        return
    collection = get_collection()
    collection.add(
        ids=ids,
        documents=documents,
        embeddings=embeddings,
        metadatas=metadatas or [{}] * len(ids),
    )
    logger.info("Added %d chunks to vector store", len(ids))


def search_similar(
    query_embedding: List[float],
    top_k: int | None = None,
) -> List[dict]:
    """检索与查询向量最相似的文档块。

    Args:
        query_embedding: 查询向量。
        top_k: 返回数量，默认使用配置值 RAG_TOP_K。

    Returns:
        结果列表，每项包含 id、document、metadata、distance。
    """
    if top_k is None:
        top_k = RAG_TOP_K
    collection = get_collection()

    if collection.count() == 0:
        logger.warning("Vector store is empty, returning no results")
        return []

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=min(top_k, collection.count()),
    )

    # ChromaDB 返回的列表包裹了一层，展开
    return [
        {
            "id": results["ids"][0][i],
            "document": results["documents"][0][i],
            "metadata": results["metadatas"][0][i],
            "distance": results["distances"][0][i],
        }
        for i in range(len(results["ids"][0]))
    ]


def get_store_count() -> int:
    """返回向量存储中的文档块数量。"""
    return get_collection().count()


def clear_store() -> None:
    """清空向量存储（调试用）。"""
    client = _get_client()
    try:
        client.delete_collection(COLLECTION_NAME)
        logger.info("Collection '%s' deleted", COLLECTION_NAME)
    except Exception:
        pass
    global _collection
    _collection = None
