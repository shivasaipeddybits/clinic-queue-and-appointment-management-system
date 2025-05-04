from pydantic import BaseModel

class PatientCreate(BaseModel):
    name: str
    email: str
    phone: str
    password: str

class PatientOut(BaseModel):
    id: int
    name: str
    email: str
    phone: str

    class Config:
        orm_mode = True
