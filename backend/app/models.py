from sqlalchemy import Column, Integer, String, Text, TIMESTAMP, ForeignKey, CheckConstraint, Date
from sqlalchemy.orm import relationship
from .database import Base

class Customer(Base):
    __tablename__ = "customers"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(150), nullable=False)
    email = Column(String(150), unique=True, nullable=False)
    phone = Column(String(20))
    portal_password_hash = Column(Text)
    created_at = Column(TIMESTAMP)

class SRF(Base):
    __tablename__ = "srfs"
    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("customers.id", ondelete="CASCADE"), nullable=False)
    srf_number = Column(String(50), unique=True, nullable=False)
    created_at = Column(TIMESTAMP)

class SRFEquipment(Base):
    __tablename__ = "srf_equipments"
    id = Column(Integer, primary_key=True, index=True)
    srf_id = Column(Integer, ForeignKey("srfs.id", ondelete="CASCADE"), nullable=False)
    equipment_name = Column(String(100), nullable=False)
    equipment_serial = Column(String(100))
    calibration_due = Column(Date)
    created_at = Column(TIMESTAMP)

class Deviation(Base):
    __tablename__ = "deviations"
    id = Column(Integer, primary_key=True, index=True)
    srf_id = Column(Integer, ForeignKey("srfs.id", ondelete="CASCADE"), nullable=False)
    equipment_id = Column(Integer, ForeignKey("srf_equipments.id", ondelete="CASCADE"), nullable=False)
    deviation_type = Column(String(50), nullable=False)
    description = Column(Text)
    status = Column(String(30), default="OPEN")
    raised_by = Column(Integer, nullable=False)
    resolved_by = Column(Integer)
    customer_action_note = Column(Text)
    resolution_notes = Column(Text)
    created_at = Column(TIMESTAMP)
    updated_at = Column(TIMESTAMP)
    resolved_at = Column(TIMESTAMP)

class Job(Base):
    __tablename__ = "jobs"
    id = Column(Integer, primary_key=True, index=True)
    equipment_id = Column(Integer, ForeignKey("srf_equipments.id", ondelete="CASCADE"), nullable=False)
    deviation_id = Column(Integer, ForeignKey("deviations.id", ondelete="SET NULL"))
    job_type = Column(String(50), nullable=False)
    status = Column(String(30), default="PENDING")
    assigned_to = Column(Integer)
    created_at = Column(TIMESTAMP)
    completed_at = Column(TIMESTAMP)

class Notification(Base):
    __tablename__ = "notifications"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)
    deviation_id = Column(Integer, ForeignKey("deviations.id", ondelete="CASCADE"))
    message = Column(Text, nullable=False)
    channel = Column(String(20), nullable=False)
    status = Column(String(20), default="PENDING")
    created_at = Column(TIMESTAMP)
    sent_at = Column(TIMESTAMP)

class Certification(Base):
    __tablename__ = "certifications"
    id = Column(Integer, primary_key=True, index=True)
    srf_id = Column(Integer, ForeignKey("srfs.id", ondelete="CASCADE"), nullable=False)
    equipment_id = Column(Integer, ForeignKey("srf_equipments.id", ondelete="CASCADE"), nullable=False)
    deviation_id = Column(Integer, ForeignKey("deviations.id", ondelete="SET NULL"))
    certificate_number = Column(String(100), unique=True)
    issued_date = Column(TIMESTAMP)
    expiry_date = Column(TIMESTAMP)
    created_at = Column(TIMESTAMP)
