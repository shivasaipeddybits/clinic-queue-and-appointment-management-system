from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import Base, engine, SessionLocal
import models, crud, schemas
import aiohttp
import os
from dotenv import load_dotenv
import asyncio

load_dotenv()
app = FastAPI()
Base.metadata.create_all(bind=engine)

NOTIFICATION_SERVICE_URL = os.getenv("NOTIFICATION_SERVICE_URL")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/appointments/book", response_model=schemas.AppointmentCreate)
async def book_appointment(appt: schemas.AppointmentCreate, db: Session = Depends(get_db)):
    try:
        appointment = crud.create_appointment(db, appt)
        asyncio.create_task(notify_user(appointment.id, db))
        return appointment
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/appointments/{patient_id}", response_model=list[schemas.AppointmentOut])
def list_appointments(patient_id : str, db: Session = Depends(get_db)):
    return crud.get_appointments(db, patient_id)

async def notify_user(appointment_id : int, db: Session):
    result = crud.get_appointment_details(db, appointment_id)
    if result:
        print(result)
        to = result.patient_email
        message = (
            f"Hello {result.patient_name}, Your appointment with Dr. {result.doctor_name} is booked on {result.appointment_time}. They are one of the greatest {result.doctor_specialization} of India. Thank you for trusting us."
        )
        payload = {"to": to, "subject": "Clinic Appointment Booked", "message": message}
        print ("I am at before async aiohttp function..")
        async with aiohttp.ClientSession() as session:
            print ("Entered aiohttp..")
            async with session.post(NOTIFICATION_SERVICE_URL, json=payload) as resp:
                print("Mail Notification Status : ", resp.status)
