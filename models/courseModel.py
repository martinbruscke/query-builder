from sqlalchemy import column
from sqlalchemy.schema import Column, UniqueConstraint
from sqlalchemy.types import String, BigInteger, Boolean, Float, Integer
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.ext.mutable import MutableDict

import uuid

from database import Base


class Course(Base):
    __tablename__ = "courses"

    uuid = Column(
        primary_key=True,
        unique=True,
        index=True,
        default=uuid.uuid4
    )
    customer_uuid = Column(String, index=True)
    course_id = Column(String, index=True)
    name = Column(String)
    course_code = Column(String)
    sis_course_id = Column(String)
    account_id = Column(BigInteger)
    root_account_id = Column(BigInteger)
    enrollment_term_id = Column(String)
    start_at = Column(BigInteger)
    end_at = Column(BigInteger)
    course_created_at = Column(BigInteger)
    time_zone = Column(String)
    term_uuid = Column(String, ForeignKey("terms.uuid"))
    is_active = Column(Boolean)
    fetched = Column(Boolean)
    lms_uuid = Column(UUID(as_uuid=True), ForeignKey('lms.uuid'))
    configuration = Column(MutableDict.as_mutable(JSONB))
    current_risk = Column(Float)
    current_risk_json = Column(String)
    activity = Column(String) 
    avg_score_grade = Column(Float)
    activity_json = Column(String)
    total_students = Column(Integer)
    total_teachers = Column(Integer)
    conclude_at = Column(BigInteger)
    enrollment_sync = Column(Boolean)
    external_id = Column(String)
    updating = Column(Boolean)
    workflow_state = Column(String)
    lms_state_uuid = Column(String)
    low_risk = Column(Float)
    high_risk = Column(Float)
    applied_rules = Column(MutableDict.as_mutable(JSONB))
    is_running = Column(Boolean)

    # Trends
    risk_trend = Column(Float)
    score_trend = Column(Float)
    activity_trend = Column(Float)

    created_at = Column(BigInteger)
    updated_at = Column(BigInteger)
    last_activity_at = Column(BigInteger)
    activity_updated_at = Column(BigInteger)

    risk_history = Column(Boolean)

    term_rel = relationship('Term')
    student_rel = relationship('StudentCourseModel', back_populates='course_rel')
    teacher_rel = relationship('TeacherCourseModel', back_populates='course_rel')
    cathedra_rel = relationship('Cathedra', back_populates='course_rel')
    assigment_rel = relationship('AssignmentModel', back_populates='course_rel')
    lesson_rel = relationship('Lessons', back_populates='course_rel')
    submission_rel = relationship('Submission', back_populates='course_rel')
    submission_history_rel = relationship('SubmissionHistory', back_populates='course_rel')
    last_login_history_rel = relationship('LastLoginHistory', back_populates="course_rel")
    courses_sync_rel = relationship('CoursesSync', back_populates='course_rel')
    tag_rel = relationship('CourseTagModel', back_populates='course_rel')

    courses_cathedras_rel = relationship('CoursesCathedrasModel', back_populates='course_rel')

    UniqueConstraint('customer_uuid', 'course_id', 'lms_uuid', name='unique_customer_course_lms')