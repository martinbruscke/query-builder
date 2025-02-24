import uuid

from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.ext.mutable import MutableDict
from sqlalchemy.schema import Column, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.types import String, BigInteger, Boolean, ARRAY, Float
from sqlalchemy.dialects.postgresql import UUID

from database import Base



class AssignmentModel(Base):
    __tablename__ = "assignments"

    uuid = Column(default=uuid.uuid4, primary_key=True, unique=True, index=True)
    assignment_id = Column(String)
    customer_uuid = Column(String, index=True)
    course_uuid = Column(String, ForeignKey("courses.uuid"))
    name = Column(String)
    due_at = Column(BigInteger)
    unlock_at = Column(BigInteger)
    lock_at = Column(BigInteger)
    assignment_group_id = Column(String)
    grading_type = Column(String)
    points_possible = Column(Float)
    position = Column(BigInteger)
    allowed_attempts = Column(BigInteger)
    omit_from_final_grade = Column(Boolean)
    submission_types = Column(ARRAY(String))
    assignment_updated_at = Column(BigInteger)
    assignment_created_at = Column(BigInteger)
    created_at = Column(BigInteger)
    updated_at = Column(BigInteger)
    lesson_uuid = Column(UUID(as_uuid=True), ForeignKey("lessons.uuid"))
    weight = Column(String)
    is_required = Column(Boolean)
    is_active = Column(Boolean)
    assignment_type = Column(String)
    can_update = Column(Boolean)

    applied_rules = Column(MutableDict.as_mutable(JSONB))

    course_rel = relationship("Course", back_populates="assigment_rel")
    lesson_rel = relationship("Lessons", back_populates="assigment_rel")
    submission_rel = relationship("Submission", back_populates="assignment_rel")
    submission_history_rel = relationship("SubmissionHistory", back_populates="assignment_rel")

    UniqueConstraint("customer_uuid", "course_uuid", "assignment_id", name="unique_customer_course_assignment_id")