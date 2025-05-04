from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import Base, engine, SessionLocal
import models, crud, schemas

app = FastAPI()
Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/patients/", response_model=schemas.PatientOut)
def register_patient(patient: schemas.PatientCreate, db: Session = Depends(get_db)):
    db_patient = crud.get_patient_by_email(db, patient.email, patient.password)
    if db_patient:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_patient(db, patient)


@app.get("/patients/verify", response_model=schemas.PatientOut)
def verify_patient(email: str, password: str, db: Session = Depends(get_db)):
    patient = crud.get_patient_by_email(db, email, password)
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    return patient

@app.get("/patients/{patient_id}", response_model=schemas.PatientOut)
def verify_patient(patient_id: int, db: Session = Depends(get_db)):
    patient = crud.get_patient_by_id(db, patient_id)
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    return patient