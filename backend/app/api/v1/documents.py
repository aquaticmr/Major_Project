from typing import List
from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, status
from sqlalchemy.orm import Session

from backend.app.core.security import get_current_user
from backend.app.db.session import get_db
from backend.app.db.models import User, Document
from backend.app.services.document_service import document_service
from backend.app.services.retrieval_service import retrieval_service
from backend.app.schemas.all_schemas import DocumentResponse

router = APIRouter()

@router.post("/upload", response_model=DocumentResponse)
async def upload_document(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Upload and process a sensitive financial document with AES-256 encryption."""
    content = await file.read()
    if len(content) == 0:
        raise HTTPException(status_code=400, detail="Uploaded file is empty.")

    try:
        doc = document_service.process_and_index_document(
            db=db,
            user_id=current_user.id,
            original_filename=file.filename,
            file_bytes=content
        )
        return doc
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Processing error: {str(e)}")

@router.get("", response_model=List[DocumentResponse])
async def list_documents(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """List documents belonging to the authenticated user."""
    return db.query(Document).filter(Document.user_id == current_user.id).order_by(Document.created_at.desc()).all()

@router.get("/{document_id}", response_model=DocumentResponse)
async def get_document(
    document_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Retrieve an owned document by ID."""
    doc = db.query(Document).filter(Document.id == document_id, Document.user_id == current_user.id).first()
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found or access unauthorized.")
    return doc

@router.delete("/{document_id}")
async def delete_document(
    document_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete an owned document and its vector embeddings."""
    doc = db.query(Document).filter(Document.id == document_id, Document.user_id == current_user.id).first()
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found or access unauthorized.")

    retrieval_service.delete_document_chunks(document_id)
    db.delete(doc)
    db.commit()
    return {"status": "success", "message": f"Document {document_id} deleted"}
