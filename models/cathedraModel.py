from sqlalchemy.schema import Column, UniqueConstraint
from sqlalchemy.types import String, BigInteger
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey

import uuid

from database import Base


class Cathedra(Base):
    __tablename__ = "cathedras"

    uuid = Column(
        primary_key=True,
        unique=True,
        index=True,
        default=uuid.uuid4
    )
    customer_uuid = Column(String, index=True)
    cathedra_id = Column(String, index=True)
    course_uuid = Column(String, ForeignKey("courses.uuid"), index=True)
    name = Column(String)
    start_at = Column(BigInteger)
    end_at = Column(BigInteger)
    cathedra_created_at = Column(BigInteger)
    sis_section_id = Column(String)
    sis_course_id = Column(String)
    created_at = Column(BigInteger)
    updated_at = Column(BigInteger)

    
    course_rel = relationship('Course', back_populates='cathedra_rel')
    student_rel = relationship('StudentCourseModel', back_populates="cathedra_rel")
    tag_rel = relationship('CourseTagModel', back_populates='cathedra_rel')

    courses_cathedras_rel = relationship('CoursesCathedrasModel', back_populates='cathedra_rel')

    UniqueConstraint('customer_uuid', 'cathedra_id', name='fk_unique_customer_cathedra_id')