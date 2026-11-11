from pydantic import BaseModel, ConfigDict, Field

class CourseCreate(BaseModel):
    course_code: str = Field(min_length=2, max_length=30)
    title: str = Field(min_length=2, max_length=150)
    description: str | None = None

class CourseUpdate(BaseModel):
    course_code: str | None = Field(default=None, min_length=2, max_length=30)
    title: str | None = Field(default=None, min_length=2, max_length=150)
    description: str | None = None

class CourseRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    course_code: str
    title: str
    description: str | None
