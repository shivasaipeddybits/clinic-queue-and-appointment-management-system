from pydantic import BaseModel

class AppointmentCreate(BaseModel):
    patient_id: int
    doctor_id: int
    appointment_time: str  # e.g., "2025-04-15 10:30"

class AppointmentOut(BaseModel):
    id: int
    doctor_id : int
    doctor_name : str
    specialization : str
    appointment_time: str
    status: str

    class Config:
        orm_mode = True
