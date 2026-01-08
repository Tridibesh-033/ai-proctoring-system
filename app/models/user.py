from sqlalchemy import Column, Integer, String
from app.database import Base
import uuid
from sqlalchemy.dialects.postgresql import UUID

class User(Base):
    __tablename__ = "users"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        index=True
    )
    email = Column(String, unique=True, index=True)
    password = Column(String,nullable=False)
    role = Column(String,nullable=False)    # recruiter / candidate
