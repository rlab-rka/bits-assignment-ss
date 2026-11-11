from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column
from .database import Base

class Enrollment(Base):
    __tablename__ = "enrollments"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    student_id: Mapped[str] = mapped_column(String(40), index=True, nullable=False)
    student_name: Mapped[str] = mapped_column(String(150), nullable=False)
    course_id: Mapped[int] = mapped_column(Integer, index=True, nullable=False)
    course_title: Mapped[str] = mapped_column(String(150), nullable=False)
    status: Mapped[str] = mapped_column(String(20), default="ACTIVE", nullable=False)
