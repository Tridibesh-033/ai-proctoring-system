import uuid
from sqlalchemy import Column, String, ForeignKey, Float, Enum
from sqlalchemy.dialects.postgresql import UUID
from app.database import Base

class Resume(Base):
    __tablename__ = "resumes"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        index=True
    )

    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id"),
        nullable=False
    )

    job_id = Column(
        UUID(as_uuid=True),
        ForeignKey("jobs.id"),
        nullable=False
    )

    file_path = Column(String, nullable=False)

    score= Column(Float, default=0.0)

    status = Column(String, default="pending")

