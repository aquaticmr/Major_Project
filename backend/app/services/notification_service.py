import uuid
from typing import List
from sqlalchemy.orm import Session
from backend.app.db.models import AlertNotification

class NotificationService:
    def create_alert(self, db: Session, user_id: str, title: str, message: str, alert_type: str = "info") -> AlertNotification:
        alert = AlertNotification(
            id=str(uuid.uuid4()),
            user_id=user_id,
            title=title,
            message=message,
            alert_type=alert_type,
            is_read=False
        )
        db.add(alert)
        db.commit()
        db.refresh(alert)
        return alert

    def get_user_alerts(self, db: Session, user_id: str) -> List[AlertNotification]:
        return db.query(AlertNotification).filter(AlertNotification.user_id == user_id).order_by(AlertNotification.created_at.desc()).all()

notification_service = NotificationService()
