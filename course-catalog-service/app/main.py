from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from .database import Base, engine, get_db
from .models import Course
from .schemas import CourseCreate, CourseUpdate, CourseRead

@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield

app = FastAPI(
    title="Course Catalog Service",
    description="Maintains the university course catalogue.",
    version="1.0.0",
    lifespan=lifespan,
)

@app.get("/health")
def health():
    return {"status": "healthy", "service": "course-catalog"}

@app.post("/courses", response_model=CourseRead, status_code=status.HTTP_201_CREATED)
def create_course(payload: CourseCreate, db: Session = Depends(get_db)):
    course = Course(**payload.model_dump())
    db.add(course)
    try:
        db.commit()
        db.refresh(course)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="Course code already exists")
    return course

@app.get("/courses", response_model=list[CourseRead])
def list_courses(db: Session = Depends(get_db)):
    return db.query(Course).order_by(Course.id).all()

@app.get("/courses/{course_id}", response_model=CourseRead)
def get_course(course_id: int, db: Session = Depends(get_db)):
    course = db.get(Course, course_id)
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    return course

@app.put("/courses/{course_id}", response_model=CourseRead)
def update_course(course_id: int, payload: CourseUpdate, db: Session = Depends(get_db)):
    course = db.get(Course, course_id)
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(course, key, value)
    try:
        db.commit()
        db.refresh(course)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="Course code already exists")
    return course

@app.delete("/courses/{course_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_course(course_id: int, db: Session = Depends(get_db)):
    course = db.get(Course, course_id)
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    db.delete(course)
    db.commit()
    return None
