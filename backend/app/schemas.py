from pydantic import BaseModel, Field, EmailStr
from typing import Optional, Literal, List

DeviationType = Literal['OOT','DAMAGED','MISSING_STANDARD','GB_FAILURE']
DeviationStatus = Literal['OPEN','IN_REVIEW','CUSTOMER_ACCEPTED','CUSTOMER_REJECTED','RESOLVED','CLOSED']

class DeviationCreate(BaseModel):
    srf_id: int
    equipment_id: int
    deviation_type: DeviationType
    description: Optional[str] = None
    raised_by: int  # current user id

class DeviationOut(BaseModel):
    id: int
    srf_id: int
    equipment_id: int
    deviation_type: str
    description: Optional[str]
    status: str
    raised_by: int
    resolved_by: Optional[int]
    customer_action_note: Optional[str]
    resolution_notes: Optional[str]

    class Config:
        from_attributes = True

class DeviationActionNote(BaseModel):
    note: Optional[str] = None

class DeviationReject(BaseModel):
    reason: str

class Customer(BaseModel):
    id: int
    name: str
    email: EmailStr
    class Config:
        from_attributes = True
