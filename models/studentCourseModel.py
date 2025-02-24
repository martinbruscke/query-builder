from sqlalchemy.orm import relationship
from sqlalchemy.schema import Column, UniqueConstraint
from sqlalchemy.types import String, BigInteger, Boolean, Float, INTEGER
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.ext.mutable import MutableDict
from sqlalchemy import ForeignKey
import uuid, time

from database import Base


class StudentCourseModel(Base):
    __tablename__ = "student_course"

    uuid = Column(default=uuid.uuid4, primary_key=True, unique=True, index=True)
    customer_uuid = Column(String)
    course_uuid = Column(String, ForeignKey("courses.uuid"))
    cathedra_uuid = Column(String, ForeignKey("cathedras.uuid"), index=True)
    user_uuid = Column(String, ForeignKey("users.uuid"))
    final_score = Column(String)
    final_score_grade = Column(String)
    current_score = Column(Float)
    relation_updated_at = Column(BigInteger)
    relation_created_at = Column(BigInteger)
    last_activity_at = Column(BigInteger)

    # Activity
    activity = Column(String)
    activity_points = Column(BigInteger)
    past_activity = Column(String)

    term_uuid = Column(String)
    last_submission_at = Column(BigInteger)
    last_login_at = Column(BigInteger)

    # Risk Detector
    current_risk = Column(Float)
    internal_risk = Column(Float)
    past_risk = Column(Float)
    risk_version = Column(String)
    risk_cause = Column(String)
    risk_rule_uuid = Column(String)
    risk_updated_at = Column(BigInteger)

    # Trends
    risk_trend = Column(Float)
    score_trend = Column(Float)
    activity_trend = Column(Float)

    is_active = Column(Boolean)

    created_at = Column(BigInteger)
    updated_at = Column(BigInteger)
    activity_updated_at = Column(BigInteger)
    last_enrollment_sync_at = Column(BigInteger)

    presences = Column(INTEGER)
    tardies = Column(INTEGER)
    absences = Column(INTEGER)
    attendance_percent = Column(Float)

    # Custom Fields
    custom_fields = Column(MutableDict.as_mutable(JSONB))

    course_rel = relationship("Course", back_populates="student_rel")
    user_rel = relationship("UserModel", back_populates="student_rel")
    cathedra_rel = relationship("Cathedra", back_populates="student_rel")

    UniqueConstraint('customer_uuid', 'course_uuid', 'cathedra_uuid', 'user_uuid', name='student_course_unique')