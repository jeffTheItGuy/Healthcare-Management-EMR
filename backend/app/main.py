from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import auth, patients, appointments, medical_records, admissions
from app.routers import lab, pharmacy, billing, staff, search

app = FastAPI(
    title="ZimEMR API",
    description="Zimbabwe Hospital Management System",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200", "https://yourdomain.co.zw"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(patients.router, prefix="/patients", tags=["Patients"])
app.include_router(appointments.router, prefix="/appointments", tags=["Appointments"])
app.include_router(medical_records.router, prefix="/records", tags=["Medical Records"])
app.include_router(admissions.router, prefix="/admissions", tags=["Admissions"])
app.include_router(lab.router, prefix="/lab", tags=["Laboratory"])
app.include_router(pharmacy.router, prefix="/pharmacy", tags=["Pharmacy"])
app.include_router(billing.router, prefix="/billing", tags=["Billing"])
app.include_router(staff.router, prefix="/staff", tags=["Staff"])
app.include_router(search.router, prefix="/search", tags=["Semantic Search"])

@app.get("/health")
def health_check():
    return {"status": "ok", "region": "ZW"}