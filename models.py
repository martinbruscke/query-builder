from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime
from sqlalchemy.dialects.postgresql import UUID
from database import Base
import uuid
from datetime import datetime

class User(Base):
    __tablename__ = "user"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    name = Column(String, index=True)
    lastname = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    phone = Column(String, unique=True, index=True)
    is_teacher = Column(Boolean, default=False)

class Course(Base):
    __tablename__ = "course"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    name = Column(String, index=True)
    teacher_id = Column(UUID(as_uuid=True), ForeignKey("user.id"), index=True)
    status = Column(String)

class StudentCourse(Base):
    __tablename__ = "student_course"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    is_active = Column(Boolean, default=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("user.id"), index=True)
    course_id = Column(UUID(as_uuid=True), ForeignKey("course.id"), index=True)

class TeacherCourse(Base):
    __tablename__ = "teacher_course"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("user.id"), index=True)
    course_id = Column(UUID(as_uuid=True), ForeignKey("course.id"), index=True)

class Assignment(Base):
    __tablename__ = "assignment"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    title = Column(String, index=True)
    description = Column(String)
    due_date = Column(DateTime)
    course_id = Column(UUID(as_uuid=True), ForeignKey("course.id"), index=True)

class Submission(Base):
    __tablename__ = "submission"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("user.id"), index=True)
    assignment_id = Column(UUID(as_uuid=True), ForeignKey("assignment.id"), index=True)
    submitted_at = Column(DateTime, default=datetime.utcnow)
    content = Column(String)
    
    
"""

Por ejemplo, si quieres obtener todas las submissions de un usuario 
junto con la información del assignment y el curso, 
podrías hacer algo como esto:


from sqlalchemy import select
from models import User, Submission, Assignment, Course

query = select(User, Submission, Assignment, Course)
    .join(
        Submission, User.id == Submission.user_id)
    .join(
        Assignment, Submission.assignment_id == Assignment.id)
    .join(
        Course, Assignment.course_id == Course.id)

# Ejecuta la consulta
result = session.execute(query).fetchall()

"""