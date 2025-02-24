from sqlalchemy.orm import relationship
from sqlalchemy.schema import Column, UniqueConstraint
from sqlalchemy.types import String, BigInteger, BigInteger, Boolean, ARRAY, Float
from sqlalchemy import ForeignKey
import uuid, time

from database import Base


class TeacherCourseModel(Base):
    __tablename__ = "teacher_course"

    uuid = Column(
        default=uuid.uuid4,
        primary_key=True,
        unique=True,
        index=True
    )
    customer_uuid = Column(String)
    course_uuid = Column(String, ForeignKey('courses.uuid'))
    cathedra_uuid = Column(String, index=True)
    user_uuid = Column(String, ForeignKey('users.uuid'))
    relation_created_at = Column(BigInteger)
    enrollment_type = Column(String)
    created_at = Column(BigInteger)
    updated_at = Column(BigInteger)
    last_enrollment_sync_at = Column(BigInteger)
    is_active = Column(Boolean)
    current_risk = Column(Float)
    last_login_at = Column(BigInteger)

    course_rel = relationship('Course', back_populates='teacher_rel')
    user_rel = relationship('UserModel', back_populates="teacher_rel")

    UniqueConstraint('customer_uuid', 'course_uuid', 'cathedra_uuid', 'user_uuid', 'enrollment_type', name='teacher_course_unique')