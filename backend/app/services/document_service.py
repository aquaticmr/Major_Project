import os
import uuid
import re
from typing import List, Dict, Any, Tuple
from datetime import datetime
import fitz # PyMuPDF
from docx import Document as DocxDocument
from sqlalchemy.orm import Session

from backend.app.core.config import settings
from backend.app.core.logging import logger
from backend.app.db.models import Document, DocumentChunk
from backend.app.services.encryption_service import encryption_service

class DocumentService:
    def __init__(self, storage_dir: str = settings.DOCUMENT_STORAGE_DIR):
        self.storage_dir = storage_dir
        os.makedirs(self.storage_dir, exist_ok=True)

    def save_and_encrypt_file(self, file_bytes: bytes, original_filename: str) -> Tuple[str, str]:
        doc_id = str(uuid.uuid4())
        ext = os.path.splitext(original_filename)[1].lower()
        stored_filename = f"{doc_id}{ext}.enc"
        file_path = os.path.join(self.storage_dir, stored_filename)

        encrypted_data = encryption_service.encrypt_bytes(file_bytes)
        with open(file_path, "wb") as f:
            f.write(encrypted_data)

        return doc_id, file_path

    def read_decrypted_file(self, file_path: str) -> bytes:
        with open(file_path, "rb") as f:
            encrypted_data = f.read()
        return encryption_service.decrypt_bytes(encrypted_data)

    def extract_text_from_pdf(self, file_bytes: bytes) -> List[Dict[str, Any]]:
        pages_content = []
        doc = fitz.open(stream=file_bytes, filetype="pdf")
        for page_idx in range(len(doc)):
            page = doc[page_idx]
            text = page.get_text()
            pages_content.append({
                "page_number": page_idx + 1,
                "text": text,
                "method": "pymupdf_text"
            })
        return pages_content

    def extract_text_from_docx(self, file_bytes: bytes) -> List[Dict[str, Any]]:
        import io
        doc = DocxDocument(io.BytesIO(file_bytes))
        full_text = "\n".join([p.text for p in doc.paragraphs if p.text.strip()])
        return [{
            "page_number": 1,
            "text": full_text,
            "method": "python_docx"
        }]

    def extract_text_from_txt(self, file_bytes: bytes) -> List[Dict[str, Any]]:
        text = file_bytes.decode("utf-8", errors="replace")
        return [{
            "page_number": 1,
            "text": text,
            "method": "plain_text"
        }]

    def chunk_document_pages(self, pages: List[Dict[str, Any]], max_chunk_words: int = 250) -> List[Dict[str, Any]]:
        chunks = []
        chunk_idx = 0
        for page_data in pages:
            page_num = page_data["page_number"]
            text = page_data["text"]
            method = page_data["method"]

            # Split text by double newlines or clause boundaries (e.g., Section 1, Clause 2, Article)
            paragraphs = re.split(r"\n\s*\n", text)
            current_chunk_words = []
            clause_id = None

            for para in paragraphs:
                para = para.strip()
                if not para:
                    continue

                # Check for clause / section header
                header_match = re.match(r"^(Section|Clause|Article|Term)\s+([0-9\.\w]+)", para, re.IGNORECASE)
                if header_match:
                    clause_id = f"{header_match.group(1)}_{header_match.group(2)}"

                words = para.split()
                if len(current_chunk_words) + len(words) > max_chunk_words and current_chunk_words:
                    chunks.append({
                        "chunk_index": chunk_idx,
                        "page_number": page_num,
                        "clause_id": clause_id or f"Page{page_num}_Clause{chunk_idx}",
                        "content": " ".join(current_chunk_words),
                        "method": method
                    })
                    chunk_idx += 1
                    current_chunk_words = []

                current_chunk_words.extend(words)

            if current_chunk_words:
                chunks.append({
                    "chunk_index": chunk_idx,
                    "page_number": page_num,
                    "clause_id": clause_id or f"Page{page_num}_Clause{chunk_idx}",
                    "content": " ".join(current_chunk_words),
                    "method": method
                })
                chunk_idx += 1

        return chunks

    def process_and_index_document(self, db: Session, user_id: str, original_filename: str, file_bytes: bytes) -> Document:
        ext = os.path.splitext(original_filename)[1].lower().replace(".", "")
        if ext not in ["pdf", "txt", "docx"]:
            raise ValueError(f"Unsupported file type: {ext}")

        doc_id, file_path = self.save_and_encrypt_file(file_bytes, original_filename)

        # Extract text based on file format
        if ext == "pdf":
            pages = self.extract_text_from_pdf(file_bytes)
            extraction_method = "pymupdf_layout"
        elif ext == "docx":
            pages = self.extract_text_from_docx(file_bytes)
            extraction_method = "python_docx"
        else:
            pages = self.extract_text_from_txt(file_bytes)
            extraction_method = "plain_text"

        page_count = len(pages)
        raw_chunks = self.chunk_document_pages(pages)

        # Persist Document entity
        doc_record = Document(
            id=doc_id,
            user_id=user_id,
            filename=original_filename,
            file_type=ext,
            file_path=file_path,
            file_size=len(file_bytes),
            page_count=page_count,
            status="indexed",
            extraction_method=extraction_method,
            is_encrypted=True,
            chunk_count=len(raw_chunks),
            meta_info={"uploaded_at": datetime.utcnow().isoformat()}
        )
        db.add(doc_record)
        db.commit()

        # Persist chunks
        db_chunks = []
        for rc in raw_chunks:
            chunk = DocumentChunk(
                document_id=doc_id,
                page_number=rc["page_number"],
                clause_id=rc["clause_id"],
                chunk_index=rc["chunk_index"],
                content=rc["content"],
                extraction_method=rc["method"],
                meta_info={"user_id": user_id, "filename": original_filename}
            )
            db.add(chunk)
            db_chunks.append(chunk)
        db.commit()

        # Add to vector store
        try:
            from backend.app.services.retrieval_service import retrieval_service
            retrieval_service.index_document_chunks(user_id=user_id, doc_id=doc_id, doc_name=original_filename, chunks=raw_chunks)
        except Exception as e:
            logger.error(f"Vector indexing error: {e}")

        db.refresh(doc_record)
        return doc_record

document_service = DocumentService()
