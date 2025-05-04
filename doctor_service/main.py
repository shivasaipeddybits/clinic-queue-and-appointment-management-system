from fastapi import FastAPI, Depends
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


@app.post("/doctors/register", response_model=schemas.DoctorOut)
def register_doctor(doctor: schemas.DoctorCreate, db: Session = Depends(get_db)):
    return crud.create_doctor(db, doctor)


@app.get("/doctors", response_model=list[schemas.DoctorOut])
def list_doctors(db: Session = Depends(get_db)):
    return crud.get_all_doctors(db)


@app.get("/doctors/{id}", response_model=schemas.DoctorOut)
def list_doctor_by_id(db: Session = Depends(get_db), id = id):
    print(crud.get_doctor_by_id(db, id))
    return crud.get_doctor_by_id(db, id)