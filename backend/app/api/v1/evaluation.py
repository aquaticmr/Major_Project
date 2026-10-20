from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.app.core.security import get_current_user, get_current_admin
from backend.app.db.session import get_db
from backend.app.db.models import User, RAGASEvaluationRun
from backend.app.services.evaluation_service import evaluation_service
from backend.app.schemas.all_schemas import EvaluationRunRequest, EvaluationRunResponse

router = APIRouter()

@router.post("/run", response_model=EvaluationRunResponse)
async def run_evaluation(
    req: EvaluationRunRequest,
    current_user: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """Trigger a genuine RAGAS / Grounding evaluation run (Admin restricted)."""
    return evaluation_service.run_ragas_evaluation(db, dataset_name=req.dataset_name)

@router.get("/history", response_model=List[EvaluationRunResponse])
async def get_evaluation_history(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Retrieve historical RAGAS benchmark evaluation runs."""
    return db.query(RAGASEvaluationRun).order_by(RAGASEvaluationRun.created_at.desc()).all()
