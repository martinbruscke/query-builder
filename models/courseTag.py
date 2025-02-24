from sqlalchemy.schema import Column
from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.types import String, TIMESTAMP, Integer
import uuid

from database import Base

class CourseTagModel(Base):
    __tablename__ = 'courses_tag'
       
    #Database Schema
    uuid = Column(
                primary_key = True,
                unique = True,
                index = True,
                default = uuid.uuid4 
    )
    customer_uuid = Column(String, index = True)
    course_uuid = Column(String, ForeignKey('courses.uuid'), index = True)
    cathedra_uuid = Column(String, ForeignKey('cathedras.uuid'), index = True)
    tag_uuid = Column(String, index = True)
    created_at = Column(TIMESTAMP)
    updated_at = Column(TIMESTAMP)

    __table_args__ = (
        UniqueConstraint('course_uuid', 'tag_uuid', name='unique_course_tag'),
    )

    course_rel = relationship('Course', back_populates='tag_rel')
    cathedra_rel = relationship('Cathedra', back_populates='tag_rel')