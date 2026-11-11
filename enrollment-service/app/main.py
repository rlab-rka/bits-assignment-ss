from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from .database import Base, engine, get_db
from .models import Enrollment
from .schemas import EnrollmentCreate, EnrollmentRead
from .course_client import fetch_course

@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield

app = FastAPI(
    title="Enrollment Management Service",
    description="Registers students for courses and manages their enrolments.",
    version="1.0.0",
    lifespan=lifespan,
)

@app.get("/health")
def health():
    return {"status": "healthy", "service": "enrollment"}

@app.post("/enrollments", response_model=EnrollmentRead, status_code=status.HTTP_201_CREATED)
def create_enrollment(payload: EnrollmentCreate, db: Session = Depends(get_db)):
    course = fetch_course(payload.course_id)
    existing = db.query(Enrollment).filter(
        Enrollment.student_id == payload.student_id,
        Enrollment.course_id == payload.course_id,
        Enrollment.status == "ACTIVE",
    ).first()
    if existing:
        raise HTTPException(status_code=409, detail="Student is already enrolled in this course")

    enrollment = Enrollment(
        student_id=payload.student_id,
        student_name=payload.student_name,
        course_id=course["id"],
        course_title=course["title"],
        status="ACTIVE",
    )
    db.add(enrollment)
    db.commit()
    db.refresh(enrollment)
    return enrollment

@app.get("/enrollments", response_model=list[EnrollmentRead])
def list_enrollments(db: Session = Depends(get_db)):
    return db.query(Enrollment).order_by(Enrollment.id).all()

@app.get("/enrollments/{enrollment_id}", response_model=EnrollmentRead)
def get_enrollment(enrollment_id: int, db: Session = Depends(get_db)):
    enrollment = db.get(Enrollment, enrollment_id)
    if not enrollment:
        raise HTTPException(status_code=404, detail="Enrollment not found")
    return enrollment

@app.get("/students/{student_id}/enrollments", response_model=list[EnrollmentRead])
def get_student_enrollments(student_id: str, db: Session = Depends(get_db)):
    return db.query(Enrollment).filter(
        Enrollment.student_id == student_id
    ).order_by(Enrollment.id).all()

@app.delete("/enrollments/{enrollment_id}", response_model=EnrollmentRead)
def cancel_enrollment(enrollment_id: int, db: Session = Depends(get_db)):
    enrollment = db.get(Enrollment, enrollment_id)
    if not enrollment:
        raise HTTPException(status_code=404, detail="Enrollment not found")
    if enrollment.status == "CANCELLED":
        raise HTTPException(status_code=409, detail="Enrollment is already cancelled")
    enrollment.status = "CANCELLED"
    db.commit()
    db.refresh(enrollment)
    return enrollment
