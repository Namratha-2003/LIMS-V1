from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime
from ..database import get_db
from .. import models, schemas
from ..state import transition
from ..notifications import queue_notification, send_email

router = APIRouter(prefix="/deviations", tags=["deviations"])

@router.post("/", response_model=schemas.DeviationOut)
def create_deviation(payload: schemas.DeviationCreate, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    # basic referential integrity checks
    srf = db.get(models.SRF, payload.srf_id)
    equip = db.get(models.SRFEquipment, payload.equipment_id)
    if not srf or not equip or equip.srf_id != srf.id:
        raise HTTPException(status_code=400, detail="Invalid SRF/Equipment relation")
    dev = models.Deviation(
        srf_id=payload.srf_id,
        equipment_id=payload.equipment_id,
        deviation_type=payload.deviation_type,
        description=payload.description,
        status="OPEN",
        raised_by=payload.raised_by,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
    )
    db.add(dev); db.commit(); db.refresh(dev)

    # notify customer (portal + email if present)
    customer = db.get(models.Customer, srf.customer_id)
    msg = f"Deviation #{dev.id} created for SRF {srf.srf_number} / Equipment {equip.equipment_name} ({payload.deviation_type})."
    queue_notification(db, user_id=customer.id, deviation_id=dev.id, message=msg, channel="PORTAL")
    if customer.email:
        background_tasks.add_task(send_email, customer.email, f"Deviation #{dev.id} Created", msg)

    return dev

@router.get("/", response_model=List[schemas.DeviationOut])
def list_deviations(db: Session = Depends(get_db)):
    return db.query(models.Deviation).order_by(models.Deviation.id.desc()).all()

@router.patch("/{dev_id}/review", response_model=schemas.DeviationOut)
def mark_in_review(dev_id: int, db: Session = Depends(get_db)):
    dev = db.get(models.Deviation, dev_id)
    if not dev:
        raise HTTPException(status_code=404, detail="Deviation not found")
    if dev.status not in ("OPEN",):
        raise HTTPException(status_code=400, detail="Only OPEN → IN_REVIEW")
    dev = transition(db, dev, "IN_REVIEW")
    # notify customer that QA is reviewing
    srf = db.get(models.SRF, dev.srf_id)
    customer = db.get(models.Customer, srf.customer_id)
    queue_notification(db, user_id=customer.id, deviation_id=dev.id, message=f"Deviation #{dev.id} is now IN_REVIEW.", channel="PORTAL")
    return dev

@router.patch("/{dev_id}/accept", response_model=schemas.DeviationOut)
def customer_accept(dev_id: int, note: schemas.DeviationActionNote, db: Session = Depends(get_db)):
    dev = db.get(models.Deviation, dev_id)
    if not dev:
        raise HTTPException(status_code=404, detail="Deviation not found")
    if dev.status not in ("IN_REVIEW",):
        raise HTTPException(status_code=400, detail="Only IN_REVIEW → CUSTOMER_ACCEPTED")
    dev.customer_action_note = note.note
    dev = transition(db, dev, "CUSTOMER_ACCEPTED")
    # notify QA
    queue_notification(db, user_id=dev.raised_by, deviation_id=dev.id, message=f"Customer ACCEPTED deviation #{dev.id}.", channel="PORTAL")
    return dev

@router.patch("/{dev_id}/reject", response_model=schemas.DeviationOut)
def customer_reject(dev_id: int, payload: schemas.DeviationReject, db: Session = Depends(get_db)):
    dev = db.get(models.Deviation, dev_id)
    if not dev:
        raise HTTPException(status_code=404, detail="Deviation not found")
    if dev.status not in ("IN_REVIEW",):
        raise HTTPException(status_code=400, detail="Only IN_REVIEW → CUSTOMER_REJECTED")
    dev.customer_action_note = payload.reason
    dev = transition(db, dev, "CUSTOMER_REJECTED")
    queue_notification(db, user_id=dev.raised_by, deviation_id=dev.id, message=f"Customer REJECTED deviation #{dev.id}.", channel="PORTAL")
    return dev

@router.patch("/{dev_id}/resolve", response_model=schemas.DeviationOut)
def qa_resolve(dev_id: int, note: schemas.DeviationActionNote, db: Session = Depends(get_db)):
    dev = db.get(models.Deviation, dev_id)
    if not dev:
        raise HTTPException(status_code=404, detail="Deviation not found")
    if dev.status not in ("CUSTOMER_ACCEPTED",):
        raise HTTPException(status_code=400, detail="Only CUSTOMER_ACCEPTED → RESOLVED")
    dev.resolution_notes = note.note
    dev.resolved_by = dev.raised_by  # demo; normally QA user id
    dev = transition(db, dev, "RESOLVED")
    return dev

@router.patch("/{dev_id}/close", response_model=schemas.DeviationOut)
def close_dev(dev_id: int, note: schemas.DeviationActionNote, db: Session = Depends(get_db)):
    dev = db.get(models.Deviation, dev_id)
    if not dev:
        raise HTTPException(status_code=404, detail="Deviation not found")
    if dev.status not in ("RESOLVED",):
        raise HTTPException(status_code=400, detail="Only RESOLVED → CLOSED")
    dev = transition(db, dev, "CLOSED")
    return dev
