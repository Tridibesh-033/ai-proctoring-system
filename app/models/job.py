from sqlalchemy import Column, Integer, String, Text, ForeignKey
from app.database import Base
import uuid
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

class Job(Base):
    __tablename__ = "jobs"


    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        index=True
    )

    title = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    company = Column(String, nullable=False)

    recruiter_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id"),
        nullable=False
    )

    recruiter = relationship("User")
