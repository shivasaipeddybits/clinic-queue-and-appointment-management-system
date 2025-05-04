from sqlalchemy.orm import Session, joinedload
from models import Appointment, Doctor, Patient
from schemas import AppointmentCreate, AppointmentOut
from dotenv import load_dotenv
import os

load_dotenv()
DOCTOR_SERVICE_URL = os.getenv("DOCTOR_SERVICE_URL")


def is_slot_taken(db: Session, doctor_id: int, appointment_time: str):
    return db.query(Appointment).filter_by(
        doctor_id=doctor_id,
        appointment_time=appointment_time
    ).first() is not None


def create_appointment(db: Session, appt: AppointmentCreate):
    if is_slot_taken(db, appt.doctor_id, appt.appointment_time):
        raise Exception("This slot is already booked for the doctor.")

    db_appt = Appointment(
        patient_id=appt.patient_id,
        doctor_id=appt.doctor_id,
        appointment_time=appt.appointment_time
    )
    db.add(db_appt)
    db.commit()
    db.refresh(db_appt)
    return db_appt


def get_appointments(db: Session, patient_id: int):
    appointment_with_doctors = db.query(Appointment, Doctor) \
        .filter(Appointment.patient_id == patient_id) \
        .join(Doctor, Appointment.doctor_id == Doctor.id)\
        .all()

    results = []
    for appointment, doctor in appointment_with_doctors:
        record = AppointmentOut(
            id=appointment.id,
            doctor_id=doctor.id,
            doctor_name=doctor.name,
            specialization=doctor.specialization,
            appointment_time=appointment.appointment_time,
            status=appointment.status
        )
        results.append(record)
    return results


def get_appointment_details(db: Session, appointment_id : int):
    return db.query(
        Appointment.id,
        Appointment.appointment_time,
        Patient.name.label("patient_name"),
        Patient.email.label("patient_email"),
        Doctor.name.label("doctor_name"),
        Doctor.specialization.label("doctor_specialization")
    ).filter(Appointment.id == appointment_id)\
    .join(Patient, Appointment.patient_id == Patient.id) \
    .join(Doctor, Appointment.doctor_id == Doctor.id) \
    .first()