from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models

router = APIRouter(prefix="/data", tags=["data"])

@router.get("/customers")
def customers(db: Session = Depends(get_db)):
    return db.query(models.Customer).all()

@router.get("/srfs")
def srfs(db: Session = Depends(get_db)):
    return db.query(models.SRF).all()

@router.get("/equipments/{srf_id}")
def equipments_for_srf(srf_id: int, db: Session = Depends(get_db)):
    return db.query(models.SRFEquipment).filter(models.SRFEquipment.srf_id==srf_id).all()
