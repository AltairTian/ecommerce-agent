"""文档摄入管线 —— 从 knowledge_base 读取文档，分块、向量化、存入 ChromaDB。"""

import logging
import re
from pathlib import Path
from typing import List

from config.settings import CHUNK_SIZE, CHUNK_OVERLAP
from src.rag.embeddings import embed_texts
from src.rag.vector_store import add_to_store, get_collection

logger = logging.getLogger("rag")

KNOWLEDGE_BASE_DIR = Path(__file__).resolve().parent / "knowledge_base"
SUPPORTED_SUFFIXES = {".md", ".txt"}


def _split_by_headings(text: str, source: str) -> List[dict]:
    """按 Markdown H2 标题分块。若无 H2，回退为按字符数分块。

    Returns:
        [{"text": "...", "metadata": {"source": ..., "heading": "...", "chunk_index": 0}}, ...]
    """
    # 按 ## 标题分割（保留标题本身）
    sections = re.split(r"\n(?=## )", text)

    chunks = []
    for i, section in enumerate(sections):
        section = section.strip()
        if not section:
            continue

        # 提取标题作为元数据
        heading_match = re.match(r"^## (.+)", section)
        heading = heading_match.group(1) if heading_match else ""

        # 如果块太大，二次切割
        if len(section) > CHUNK_SIZE:
            sub_chunks = _split_by_length(section, CHUNK_SIZE, CHUNK_OVERLAP)
            for j, sub in enumerate(sub_chunks):
                chunks.append({
                    "text": sub,
                    "metadata": {
                        "source": source,
                        "heading": heading,
                        "chunk_index": f"{i}_{j}",
                    },
                })
        else:
            chunks.append({
                "text": section,
                "metadata": {
                    "source": source,
                    "heading": heading,
                    "chunk_index": str(i),
                },
            })

    return chunks


def _split_by_length(text: str, chunk_size: int, overlap: int) -> List[str]:
    """按字符数滑动窗口分块（回退方案）。"""
    chunks = []
    start = 0
    while start < len(text):
        end = min(start + chunk_size, len(text))
        chunks.append(text[start:end])
        start += chunk_size - overlap
    return chunks


def _discover_files() -> List[Path]:
    """扫描 knowledge_base 目录，返回待摄入的文件列表。"""
    if not KNOWLEDGE_BASE_DIR.exists():
        logger.warning("Knowledge base directory not found: %s", KNOWLEDGE_BASE_DIR)
        return []
    files = [
        f for f in KNOWLEDGE_BASE_DIR.iterdir()
        if f.is_file() and f.suffix.lower() in SUPPORTED_SUFFIXES
    ]
    logger.info("Found %d file(s) to ingest", len(files))
    return files


def ingest_file(file_path: Path) -> int:
    """摄入单个文件：分块 → 向量化 → 存储。

    Returns:
        摄入的块数量。
    """
    content = file_path.read_text(encoding="utf-8")
    if not content.strip():
        return 0

    source = file_path.name
    chunk_data = _split_by_headings(content, source)

    if not chunk_data:
        return 0

    texts = [c["text"] for c in chunk_data]
    metadatas = [c["metadata"] for c in chunk_data]
    ids = [f"{source}_chunk_{c['metadata']['chunk_index']}" for c in chunk_data]

    logger.info("Embedding %d chunks from %s...", len(texts), source)
    embeddings = embed_texts(texts)

    add_to_store(ids=ids, documents=texts, embeddings=embeddings, metadatas=metadatas)
    return len(chunk_data)


def ingest_all() -> int:
    """扫描 knowledge_base 并摄入所有文档（跳过已存在的）。

    Returns:
        总摄入块数。
    """
    files = _discover_files()
    if not files:
        return 0

    # 获取已摄入的文件列表（通过 metadata 去重）
    existing_sources = set()
    try:
        collection = get_collection()
        if collection.count() > 0:
            all_meta = collection.get()["metadatas"]
            existing_sources = {m.get("source", "") for m in all_meta if m}
    except Exception:
        pass

    total = 0
    for file_path in files:
        if file_path.name in existing_sources:
            logger.info("Skipping (already ingested): %s", file_path.name)
            continue
        count = ingest_file(file_path)
        total += count
        logger.info("Ingested %s: %d chunks", file_path.name, count)

    logger.info("Ingestion complete: %d total chunks from %d files", total, len(files))
    return total
