import uuid
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.app.core.security import get_current_user
from backend.app.db.session import get_db
from backend.app.db.models import User, RAGSession, RAGMessage
from backend.app.services.rag_service import rag_service
from backend.app.schemas.all_schemas import RAGQueryRequest, RAGQueryResponse, RAGSessionResponse

router = APIRouter()

@router.post("/query", response_model=RAGQueryResponse)
async def query_rag(
    req: RAGQueryRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Query user documents with hybrid retrieval and numerical/clause verification."""
    # Ensure active session
    session_id = req.session_id
    if not session_id:
        new_session = RAGSession(user_id=current_user.id, title=req.question[:50])
        db.add(new_session)
        db.commit()
        db.refresh(new_session)
        session_id = new_session.id
    else:
        # Validate ownership of session
        existing_session = db.query(RAGSession).filter(RAGSession.id == session_id, RAGSession.user_id == current_user.id).first()
        if not existing_session:
            raise HTTPException(status_code=404, detail="Session not found or access unauthorized.")

    # Record user message
    user_msg = RAGMessage(
        session_id=session_id,
        sender="user",
        content=req.question
    )
    db.add(user_msg)
    db.commit()

    # Generate grounded response
    resp = await rag_service.query(
        question=req.question,
        user_id=current_user.id,
        session_id=session_id,
        document_ids=req.document_ids
    )

    # Record assistant message
    asst_msg = RAGMessage(
        session_id=session_id,
        sender="assistant",
        content=resp.answer,
        evidence_score=resp.evidence_score,
        verification_status=resp.verification_status,
        citations=[c.dict() for c in resp.citations],
        meta_info={"breakdown": resp.evidence_breakdown}
    )
    db.add(asst_msg)
    db.commit()

    return resp

@router.get("/sessions", response_model=List[RAGSessionResponse])
async def list_sessions(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Retrieve all RAG sessions for current user."""
    return db.query(RAGSession).filter(RAGSession.user_id == current_user.id).order_by(RAGSession.created_at.desc()).all()
