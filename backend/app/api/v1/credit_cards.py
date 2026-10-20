import json
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.app.core.security import get_current_user
from backend.app.db.session import get_db
from backend.app.db.models import User, CardRecommendationResult
from backend.app.services.credit_card_service import credit_card_service
from backend.app.schemas.all_schemas import CardRecommendationRequest, CardRecommendationResponse

router = APIRouter()

@router.post("/recommend", response_model=CardRecommendationResponse)
async def recommend_credit_cards(
    req: CardRecommendationRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Rank credit card options using trained ML model and explicit fee/reward calculations."""
    resp = credit_card_service.recommend(req.profile)

    # Persist recommendation history
    rec_record = CardRecommendationResult(
        user_id=current_user.id,
        ranked_cards=[c.dict() for c in resp.ranked_cards],
        model_version=resp.model_version
    )
    db.add(rec_record)
    db.commit()

    return resp
