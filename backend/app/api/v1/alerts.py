from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.app.core.security import get_current_user
from backend.app.db.session import get_db
from backend.app.db.models import User, AlertNotification
from backend.app.services.notification_service import notification_service
from backend.app.schemas.all_schemas import AlertResponse

router = APIRouter()

@router.get("", response_model=List[AlertResponse])
async def list_alerts(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Retrieve all notifications and security alerts for the current user."""
    return notification_service.get_user_alerts(db, current_user.id)

@router.post("/{alert_id}/read")
async def mark_alert_read(
    alert_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Mark an alert as read."""
    alert = db.query(AlertNotification).filter(AlertNotification.id == alert_id, AlertNotification.user_id == current_user.id).first()
    if alert:
        alert.is_read = True
        db.commit()
    return {"status": "success"}
