from sqlalchemy.orm import Session
from models import Patient
from schemas import PatientCreate
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_patient(db: Session, patient: PatientCreate):
    hashed_password = pwd_context.hash(patient.password)
    db_patient = Patient(
        name=patient.name,
        email=patient.email,
        phone=patient.phone,
        password_hash=hashed_password
    )
    db.add(db_patient)
    db.commit()
    db.refresh(db_patient)
    return db_patient

def get_patient_by_email(db: Session, email: str, password: str):
    hashed_password = pwd_context.hash(password)
    return db.query(Patient).filter(Patient.email == email and Patient.password_hash == hashed_password).first()

def get_patient_by_id(db: Session, patient_id: int):
    return db.query(Patient).filter(Patient.id == patient_id).first()
