import uuid
from sqlalchemy import Column, String, Text, ForeignKey, JSON
from sqlalchemy.dialects.postgresql import UUID
from app.database import Base

class ExamQuestion(Base):
    __tablename__ = "exam_questions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    exam_id = Column(UUID(as_uuid=True), ForeignKey("exams.id"), nullable=False)

    question = Column(Text, nullable=False)
    type = Column(String(20), nullable=False)  
    difficulty = Column(String(20), nullable=False)  
    options = Column(JSON, nullable=True)  
    correct_answer = Column(String, nullable=True)
   
