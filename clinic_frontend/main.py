from fastapi import FastAPI, Request, Form, Response
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from passlib.context import CryptContext
import aiohttp
from dotenv import load_dotenv
import os
import ast

load_dotenv()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

PATIENT_SERVICE_URL = os.getenv("PATIENT_SERVICE_URL")
DOCTOR_SERVICE_URL = os.getenv("DOCTOR_SERVICE_URL")
APPOINTMENT_SERVICE_URL = os.getenv("APPOINTMENT_SERVICE_URL")

# --- LOGIN PAGE ---
@app.get("/", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@app.post("/login")
async def login(request: Request, email: str = Form(...), password: str = Form(...)):
    payload = {"email": email, "password": password}

    async with aiohttp.ClientSession() as session:
        async with session.get(f"{PATIENT_SERVICE_URL}/verify", params=payload) as resp:
            if resp.status != 200:
                return templates.TemplateResponse("login.html", {"request": request, "message": "Invalid login."})
            else:
                patient = await resp.json()

    response = RedirectResponse(url="/appointments", status_code=303)
    response.set_cookie(key="patient", value=patient)
    return response


# --- REGISTER PAGE ---
@app.get("/register", response_class=HTMLResponse)
async def register_page(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})


@app.post("/register")
async def register(
        request: Request,
        name: str = Form(...),
        email: str = Form(...),
        phone: str = Form(...),
        password: str = Form(...)
):
    payload = {
        "name": name,
        "email": email,
        "phone": phone,
        "password": password
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(PATIENT_SERVICE_URL, json=payload) as resp:
            if resp.status == 200:
                response = RedirectResponse(url="/", status_code=303)
                response.set_cookie("message", "Registration Successful. Please login to continue.")
                return response
            else:
                return templates.TemplateResponse("register.html",
                                                  {"request": request, "message": "Registration failed."})


# --- BOOK APPOINTMENT PAGE ---
@app.get("/book", response_class=HTMLResponse)
async def book_page(request: Request):
    patient = ast.literal_eval(request.cookies.get("patient"))
    if not patient:
        return RedirectResponse(url="/", status_code=303)

    async with aiohttp.ClientSession() as session:
        async with session.get(DOCTOR_SERVICE_URL) as resp:
            doctors = await resp.json()

    return templates.TemplateResponse("book.html", {
        "request": request,
        "doctors": doctors,
        "patient": patient
    })


@app.post("/book")
async def book_appointment(request: Request, doctor_id: str = Form(...), appointment_time: str = Form(...)):
    patient = ast.literal_eval(request.cookies.get("patient"))
    if not patient.get("id"):
         return RedirectResponse(url="/", status_code=303)

    payload = {
        "patient_id": int(patient.get("id")),
        "doctor_id": int(doctor_id),
        "appointment_time": str(appointment_time)
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(APPOINTMENT_SERVICE_URL + "/book", json=payload) as resp:
            results = await resp.json()
            status = resp.status
            if status != 200:
                return templates.TemplateResponse("book.html", {
                    "request": request,
                    "doctors": await (await aiohttp.ClientSession().get(DOCTOR_SERVICE_URL)).json(),
                    "message": "Appointment booked successfully!" if resp.status == 200 else "Failed to book appointment. "+results["detail"],
                    "patient": patient,
                })
            else:
                response = RedirectResponse(url="/appointments", status_code=303)
                response.set_cookie(key="patient", value=patient)
                return response

# --- MY APPOINTMENT PAGE ---
@app.get("/appointments", response_class=HTMLResponse)
async def appointments_page(request: Request):
    patient = ast.literal_eval(request.cookies.get("patient"))
    if not patient:
         return RedirectResponse(url="/", status_code=303)

    async with aiohttp.ClientSession() as session:
        async with session.get(f"{APPOINTMENT_SERVICE_URL}/{patient['id']}") as resp:
            appointments = await resp.json()

    return templates.TemplateResponse("appointments.html", {
        "request": request,
        "appointments": appointments,
        "patient": patient
    })