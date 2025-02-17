from fastapi import FastAPI, HTTPException,Depends

from models import User, TeacherCourse, StudentCourse, Course,Assignment, Submission
from database import create_all_tables, get_db
from routes import query_builder_routes
from sqlalchemy.orm import Session


import uuid
from datetime import datetime, timedelta


app = FastAPI()


create_all_tables() 



# Endpoint para poblar la base de datos
@app.post("/populate_db/")
def populate_db(db: Session = Depends(get_db)):
    # Datos de ejemplo
    users = [
        User(id=uuid.uuid4(), name="Alice", lastname="Smith", email="alice@example.com", phone="1234567890", is_teacher=False),
        User(id=uuid.uuid4(), name="Bob", lastname="Brown", email="bob@example.com", phone="2345678901", is_teacher=False),
        User(id=uuid.uuid4(), name="Charlie", lastname="Davis", email="charlie@example.com", phone="3456789012", is_teacher=False),
        User(id=uuid.uuid4(), name="David", lastname="Evans", email="david@example.com", phone="4567890123", is_teacher=True),
        User(id=uuid.uuid4(), name="Eve", lastname="Foster", email="eve@example.com", phone="5678901234", is_teacher=True),
    ]

    courses = [
        Course(id=uuid.uuid4(), name="Math 101"),
        Course(id=uuid.uuid4(), name="History 201"),
    ]

    student_courses = [
        StudentCourse(is_active=True, user_id=users[0].id, course_id=courses[0].id),
        StudentCourse(is_active=True, user_id=users[1].id, course_id=courses[0].id),
        StudentCourse(is_active=True, user_id=users[2].id, course_id=courses[1].id),
    ]

    teacher_courses = [
        TeacherCourse(user_id=users[3].id, course_id=courses[0].id),
        TeacherCourse(user_id=users[4].id, course_id=courses[1].id),
    ]

    assignments = [
        Assignment(id=uuid.uuid4(), title="Assignment 1", description="Math assignment", due_date=datetime.utcnow() + timedelta(days=7), course_id=courses[0].id),
        Assignment(id=uuid.uuid4(), title="Assignment 2", description="History assignment", due_date=datetime.utcnow() + timedelta(days=7), course_id=courses[1].id),
    ]

    submissions = [
        Submission(id=uuid.uuid4(), user_id=users[0].id, assignment_id=assignments[0].id, submitted_at=datetime.utcnow(), content="Completed"),
        Submission(id=uuid.uuid4(), user_id=users[1].id, assignment_id=assignments[0].id, submitted_at=datetime.utcnow(), content="Completed"),
    ]

    # Insertar datos en la base de datos
    db.add_all(users + courses + student_courses + teacher_courses + assignments + submissions)
    db.commit()

    return {"message": "Base de datos poblada con éxito"}









app.include_router(query_builder_routes)
