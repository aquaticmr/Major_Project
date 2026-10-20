from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.app.core.security import get_current_user
from backend.app.db.session import get_db
from backend.app.db.models import User, FinancialProfile
from backend.app.services.advisory_service import advisory_service
from backend.app.schemas.all_schemas import AdvisoryAnalysisRequest, AdvisoryAnalysisResponse

router = APIRouter()

@router.post("/analyze", response_model=AdvisoryAnalysisResponse)
async def analyze_finances(
    req: AdvisoryAnalysisRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Analyze financial profile, calculate surplus, savings rate, and EMI."""
    # Persist or update latest financial profile
    p = req.profile
    profile_record = FinancialProfile(
        user_id=current_user.id,
        monthly_income=p.monthly_income,
        monthly_expenses=p.monthly_expenses,
        dining_spend=p.dining_spend,
        travel_spend=p.travel_spend,
        grocery_spend=p.grocery_spend,
        fuel_spend=p.fuel_spend,
        other_spend=p.other_spend,
        annual_fee_willingness=p.annual_fee_willingness,
        preferred_reward_type=p.preferred_reward_type,
        debt_amount=p.debt_amount
    )
    db.add(profile_record)
    db.commit()

    return advisory_service.analyze_finances(req)
