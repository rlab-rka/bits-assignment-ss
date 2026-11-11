from pydantic import BaseModel, ConfigDict, Field

class EnrollmentCreate(BaseModel):
    student_id: str = Field(min_length=2, max_length=40)
    student_name: str = Field(min_length=2, max_length=150)
    course_id: int = Field(gt=0)

class EnrollmentRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    student_id: str
    student_name: str
    course_id: int
    course_title: str
    status: str
