from datetime import datetime
from sqlalchemy.orm import Session
from . import models

def transition(db: Session, deviation: models.Deviation, new_status: str):
    deviation.status = new_status
    deviation.updated_at = datetime.utcnow()
    if new_status == 'RESOLVED':
        deviation.resolved_at = datetime.utcnow()
    db.add(deviation)
    db.commit()
    db.refresh(deviation)
    return deviation
