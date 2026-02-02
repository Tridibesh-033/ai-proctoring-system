import uuid
from sqlalchemy import Column, ForeignKey, DateTime, String, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from app.database import Base

class ExamAttempt(Base):
    __tablename__ = "exam_attempts"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    exam_id = Column(UUID(as_uuid=True), ForeignKey("exams.id"), nullable=False)
    candidate_id = Column(UUID(as_uuid=True), nullable=False)

    status = Column(
        String,
        nullable=False,
        default="STARTED"  # STARTED | SUBMITTED | EXPIRED
    )

    started_at = Column(DateTime(timezone=True), server_default=func.now())
    submitted_at = Column(DateTime(timezone=True), nullable=True)

    __table_args__ = (
        UniqueConstraint(
            "exam_id",
            "candidate_id",
            name="unique_exam_attempt_per_candidate"
        ),
    )

