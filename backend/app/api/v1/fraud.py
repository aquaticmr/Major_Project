from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.app.core.security import get_current_user
from backend.app.db.session import get_db
from backend.app.db.models import User, FraudAssessment
from backend.app.services.url_fraud_service import url_fraud_service
from backend.app.services.notification_service import notification_service
from backend.app.schemas.all_schemas import URLFraudRequest, URLFraudResponse, FraudAssessmentResponse

router = APIRouter()

@router.post("/analyze-url", response_model=URLFraudResponse)
async def analyze_url(
    req: URLFraudRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Classify a URL using the trained URL fraud Random Forest model."""
    result = url_fraud_service.analyze_url(req.url)

    # Persist assessment record
    record = FraudAssessment(
        user_id=current_user.id,
        url=req.url,
        risk_score=result.risk_score,
        is_malicious=result.is_malicious,
        explanation_factors=result.explanation_factors,
        model_version=result.model_version
    )
    db.add(record)
    db.commit()

    # Trigger alert if high risk
    if result.is_malicious:
        notification_service.create_alert(
            db=db,
            user_id=current_user.id,
            title="High-Risk Fraud URL Detected",
            message=f"Analyzed URL '{req.url[:60]}...' has risk score {result.risk_score * 100:.1f}%. Avoid interaction.",
            alert_type="danger"
        )

    return result

@router.get("/history", response_model=List[FraudAssessmentResponse])
async def get_fraud_history(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Retrieve user-specific URL assessment history."""
    return db.query(FraudAssessment).filter(FraudAssessment.user_id == current_user.id).order_by(FraudAssessment.created_at.desc()).all()
