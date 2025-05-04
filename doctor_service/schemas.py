from pydantic import BaseModel

class DoctorCreate(BaseModel):
    name: str
    specialization: str

class DoctorOut(BaseModel):
    id: int
    name: str
    specialization: str

    class Config:
        orm_mode = True
