from sqlalchemy import ForeignKey
from sqlalchemy.schema import Column, ForeignKey, UniqueConstraint
from sqlalchemy.types import String, BigInteger, Boolean, Integer, Float
from sqlalchemy.orm import relationship
import uuid

from database import Base



class UserModel(Base):
    __tablename__ = "users"

    uuid = Column(
        default=uuid.uuid4,
        primary_key=True,
        unique=True,
        index=True
    )
    user_id = Column(String)
    customer_uuid = Column(String)
    lms_uuid = Column(String, ForeignKey('lms.uuid'))
    name = Column(String)
    sortable_name = Column(String)
    short_name = Column(String)
    integration_id = Column(BigInteger)
    sis_user_id = Column(String)
    email_sis = Column(String)
    phone_sis = Column(String)
    user_created_at = Column(BigInteger)
    email = Column(String)
    is_active_student = Column(Boolean)
    is_active_teacher = Column(Boolean)
    registry_id = Column(Integer)
    master_id = Column(Integer)

    current_risk = Column(Float)
    teacher_current_risk = Column(Float)
    activity = Column(String)
    
    # Trends
    student_risk_trend = Column(Float)
    student_score_trend = Column(Float)
    student_activity_trend = Column(Float)

    teacher_risk_trend = Column(Float)
    teacher_score_trend = Column(Float)
    teacher_activity_trend = Column(Float)

    created_at = Column(BigInteger)
    updated_at = Column(BigInteger)
    last_login_at = Column(BigInteger)
    activity_updated_at = Column(BigInteger)
    avatar_url = Column(String)
    avg_final_grade = Column(Float)
    is_student = Column(Boolean)
    is_teacher = Column(Boolean)
    is_active = Column(Boolean)
    archive_attempt = Column(Integer)
    login_id = Column(String)
    location_uuid = Column(String, ForeignKey('locations.uuid'))

    xmax = Column(String, system=True)

    location_rel = relationship('LocationModel', back_populates="user_rel")
    lms_rel = relationship('LmsModel')
    student_rel = relationship('StudentCourseModel', back_populates="user_rel")
    teacher_rel = relationship('TeacherCourseModel', back_populates="user_rel")
    submission_rel = relationship('Submission', back_populates="user_rel")
    submission_history_rel = relationship('SubmissionHistory', back_populates="user_rel")
    last_login_history_rel = relationship('LastLoginHistory', back_populates="user_rel")

    UniqueConstraint('customer_uuid', 'user_id', 'lms_uuid', name='unique_customer_userid_lmsuuid')