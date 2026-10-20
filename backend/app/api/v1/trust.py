from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.app.core.security import get_current_user
from backend.app.db.session import get_db
from backend.app.db.models import User, TrustScoreAssessment
from backend.app.services.trust_score_service import trust_score_service
from backend.app.schemas.all_schemas import TrustScoreRequest, TrustScoreResponse

router = APIRouter()

@router.post("/score", response_model=TrustScoreResponse)
async def score_trust(
    req: TrustScoreRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Calculate an alternative behavioral trust score using the trained calibrated logistic regression model."""
    result = trust_score_service.calculate_score(req)

    record = TrustScoreAssessment(
        user_id=current_user.id,
        trust_score=result.trust_score,
        risk_category=result.risk_category,
        factors=result.contributing_factors,
        model_version=result.model_version
    )
    db.add(record)
    db.commit()

    return result
