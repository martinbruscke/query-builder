from sqlalchemy.schema import Column
from sqlalchemy.types import String, BigInteger, Integer, Boolean, Float
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey, UniqueConstraint
import uuid
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.ext.mutable import MutableDict

from database import Base


class Submission(Base):
    __tablename__ = "submissions"

    uuid = Column(
        primary_key=True,
        unique=True,
        index=True,
        default=uuid.uuid4
    )
    customer_uuid = Column(String, index=True)
    submissions_id = Column(BigInteger)
    assignment_uuid = Column(UUID(as_uuid=True), ForeignKey('assignments.uuid'))
    score = Column(Float)
    user_uuid = Column(UUID(as_uuid=True), ForeignKey('users.uuid'))
    course_uuid = Column(UUID(as_uuid=True), ForeignKey('courses.uuid'))
    submission_type = Column(String)
    submitted_at = Column(String)
    graded_at = Column(String)
    workflow_state = Column(String)
    grader_id = Column(BigInteger)
    grade_matches_current_submission = Column(Boolean)
    attempt = Column(Integer)
    late = Column(Boolean)
    missing = Column(Boolean)
    comment = Column(String)
    score_grade = Column(String)

    applied_rules = Column(MutableDict.as_mutable(JSONB))

    created_at = Column(BigInteger)
    updated_at = Column(BigInteger)

    course_rel = relationship('Course', back_populates='submission_rel')
    user_rel = relationship('UserModel', back_populates='submission_rel')
    assignment_rel = relationship('AssignmentModel', back_populates='submission_rel')

    UniqueConstraint('customer_uuid', 'submissions_id', name='unique_customer_submission_id')