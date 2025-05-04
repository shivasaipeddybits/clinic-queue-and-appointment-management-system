from sqlalchemy.orm import Session
from models import Doctor
from schemas import DoctorCreate

def create_doctor(db: Session, doctor: DoctorCreate):
    db_doctor = Doctor(name=doctor.name, specialization=doctor.specialization)
    db.add(db_doctor)
    db.commit()
    db.refresh(db_doctor)
    return db_doctor

def get_all_doctors(db: Session):
    return db.query(Doctor).all()

def get_doctor_by_id(db: Session, id: str):
    return db.query(Doctor).filter_by(Doctor.id==id).first()
