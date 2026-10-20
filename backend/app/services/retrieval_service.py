import os
import math
from typing import List, Dict, Any, Optional
from rank_bm25 import BM25Okapi
import chromadb
from chromadb.config import Settings as ChromaSettings

from backend.app.core.config import settings
from backend.app.core.logging import logger

class SimpleFastEmbed:
    """Fallback embedding generator using hashing/bag of words or fastembed if installed."""
    def __init__(self, dim: int = 384):
        self.dim = dim
        self._embedder = None
        try:
            from fastembed import TextEmbedding
            self._embedder = TextEmbedding()
            logger.info("FastEmbed local embedding model loaded")
        except Exception:
            logger.info("FastEmbed library not initialized; utilizing deterministic semantic feature projection")

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        if self._embedder:
            try:
                return [list(emb) for emb in self._embedder.embed(texts)]
            except Exception as e:
                logger.warning(f"FastEmbed execution error, falling back to deterministic projection: {e}")

        # Deterministic projection fallback for local dev
        embeddings = []
        for text in texts:
            vec = [0.0] * self.dim
            words = text.lower().split()
            for w in words:
                idx = abs(hash(w)) % self.dim
                vec[idx] += 1.0
            norm = math.sqrt(sum(x * x for x in vec)) or 1.0
            embeddings.append([x / norm for x in vec])
        return embeddings

    def embed_query(self, query: str) -> List[float]:
        return self.embed_documents([query])[0]

class RetrievalService:
    def __init__(self, chroma_dir: str = settings.CHROMA_PERSIST_DIR):
        self.chroma_dir = chroma_dir
        os.makedirs(self.chroma_dir, exist_ok=True)
        self.chroma_client = chromadb.PersistentClient(path=self.chroma_dir)
        self.collection = self.chroma_client.get_or_create_collection("financial_documents")
        self.embedder = SimpleFastEmbed()

    def index_document_chunks(self, user_id: str, doc_id: str, doc_name: str, chunks: List[Dict[str, Any]]):
        if not chunks:
            return

        ids = [f"{doc_id}_{c['chunk_index']}" for c in chunks]
        texts = [c["content"] for c in chunks]
        embeddings = self.embedder.embed_documents(texts)
        metadatas = [{
            "user_id": user_id,
            "document_id": doc_id,
            "document_name": doc_name,
            "page_number": int(c["page_number"]),
            "clause_id": str(c["clause_id"] or ""),
            "chunk_index": int(c["chunk_index"])
        } for c in chunks]

        self.collection.upsert(
            ids=ids,
            embeddings=embeddings,
            documents=texts,
            metadatas=metadatas
        )
        logger.info(f"Indexed {len(chunks)} chunks in ChromaDB for doc {doc_id}")

    def delete_document_chunks(self, doc_id: str):
        try:
            self.collection.delete(where={"document_id": doc_id})
        except Exception as e:
            logger.warning(f"Error deleting chunks from Chroma: {e}")

    def hybrid_search(
        self,
        query: str,
        user_id: str,
        top_k: int = 5,
        alpha: float = settings.RAG_HYBRID_ALPHA,
        document_ids: Optional[List[str]] = None
    ) -> List[Dict[str, Any]]:
        # 1. Fetch user's candidate chunks from Chroma
        where_filter: Dict[str, Any] = {"user_id": user_id}
        if document_ids and len(document_ids) == 1:
            where_filter["document_id"] = document_ids[0]

        # Fetch records
        res = self.collection.get(
            where=where_filter,
            include=["documents", "metadatas", "embeddings"]
        )

        if not res or not res["ids"]:
            return []

        doc_ids = res["ids"]
        corpus_texts = res["documents"]
        metas = res["metadatas"]
        corpus_embeddings = res["embeddings"]

        # Filter by multiple document_ids if provided
        if document_ids and len(document_ids) > 1:
            filtered_idx = [i for i, m in enumerate(metas) if m.get("document_id") in document_ids]
            if not filtered_idx:
                return []
            doc_ids = [doc_ids[i] for i in filtered_idx]
            corpus_texts = [corpus_texts[i] for i in filtered_idx]
            metas = [metas[i] for i in filtered_idx]
            corpus_embeddings = [corpus_embeddings[i] for i in filtered_idx] if corpus_embeddings else []

        # 2. BM25 Lexical Retrieval
        tokenized_corpus = [doc.lower().split() for doc in corpus_texts]
        tokenized_query = query.lower().split()
        bm25 = BM25Okapi(tokenized_corpus)
        bm25_raw_scores = bm25.get_scores(tokenized_query)
        max_bm25 = max(bm25_raw_scores) if max(bm25_raw_scores) > 0 else 1.0
        bm25_norm_scores = [score / max_bm25 for score in bm25_raw_scores]

        # 3. Dense Semantic Retrieval
        query_embedding = self.embedder.embed_query(query)
        dense_scores = []
        for emb in corpus_embeddings:
            # Cosine similarity
            dot = sum(a * b for a, b in zip(query_embedding, emb))
            norm_q = math.sqrt(sum(a * a for a in query_embedding)) or 1.0
            norm_e = math.sqrt(sum(b * b for b in emb)) or 1.0
            sim = (dot / (norm_q * norm_e) + 1.0) / 2.0 # normalize to [0, 1]
            dense_scores.append(sim)

        # 4. Hybrid Combination: S_hybrid = alpha * S_dense + (1 - alpha) * S_BM25
        results = []
        for i in range(len(doc_ids)):
            score = (alpha * dense_scores[i]) + ((1.0 - alpha) * bm25_norm_scores[i])
            results.append({
                "chunk_id": doc_ids[i],
                "document_id": metas[i].get("document_id"),
                "document_name": metas[i].get("document_name"),
                "page_number": metas[i].get("page_number"),
                "clause_id": metas[i].get("clause_id"),
                "content": corpus_texts[i],
                "hybrid_score": float(score),
                "dense_score": float(dense_scores[i]),
                "bm25_score": float(bm25_norm_scores[i])
            })

        results.sort(key=lambda x: x["hybrid_score"], reverse=True)
        return results[:top_k]

retrieval_service = RetrievalService()
