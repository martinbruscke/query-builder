from fastapi import FastAPI, HTTPException,Depends

from models.assignmentModel import AssignmentModel
from models.courseModel import User, TeacherCourse, StudentCourse, Course,Assignment, Submission
from database import create_all_tables, get_db
from models.studentCourseModel import StudentCourseModel
from models.teacherModel import TeacherCourseModel
from routes import query_builder_routes
from sqlalchemy.orm import Session


import uuid
from datetime import datetime, timedelta


app = FastAPI()


create_all_tables() 



# Endpoint para poblar la base de datos
@app.post("/populate_db/")
def populate_db(db: Session = Depends(get_db)):
    # Crear usuarios (estudiantes y profesores)
    # Ejemplo de creación de un curso
    course = Course(
        customer_uuid=str(uuid.uuid4()),
        course_id="course_001",
        name="Curso de Ejemplo",
        is_active=True,
        created_at=int(datetime.now().timestamp()),
        updated_at=int(datetime.now().timestamp())
    )
    db.add(course)

    # Crear múltiples estudiantes
    for i in range(1, 9):  # Crea 8 estudiantes
        student_course = StudentCourseModel(
            customer_uuid=str(uuid.uuid4()),
            course_uuid=course.uuid,  # Relación con el curso creado
            user_uuid=str(uuid.uuid4()),  # Asignar un UUID de usuario ficticio
            final_score="A",
            created_at=int(datetime.now().timestamp()),
            updated_at=int(datetime.now().timestamp())
        )
        db.add(student_course)

    # Crear múltiples profesores
    for i in range(1, 9):  # Crea 8 profesores
        teacher_course = TeacherCourseModel(
            customer_uuid=str(uuid.uuid4()),
            course_uuid=course.uuid,  # Relación con el curso creado
            user_uuid=str(uuid.uuid4()),  # Asignar un UUID de usuario ficticio
            created_at=int(datetime.now().timestamp()),
            updated_at=int(datetime.now().timestamp())
        )
        db.add(teacher_course)

    # Ejemplo de creación de una asignación
    assignment = AssignmentModel(
        customer_uuid=str(uuid.uuid4()),
        assignment_id="assignment_001",
        name="Tarea de Ejemplo",
        course_uuid=course.uuid,  # Relación con el curso creado
        created_at=int(datetime.now().timestamp()),
        updated_at=int(datetime.now().timestamp())
    )
    db.add(assignment)

    # Ejemplo de creación de una entrega
    submission = Submission(
        customer_uuid=str(uuid.uuid4()),
        assignment_uuid=assignment.uuid,  # Relación con la asignación creada
        user_uuid=str(uuid.uuid4()),  # Asignar un UUID de usuario ficticio
        score=95.0,
        created_at=int(datetime.now().timestamp()),
        updated_at=int(datetime.now().timestamp())
    )
    db.add(submission)

    db.commit()
    return {"message": "Base de datos poblada con éxito."}








app.include_router(query_builder_routes)
