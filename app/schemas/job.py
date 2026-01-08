from pydantic import BaseModel
from uuid import UUID

# request
class JobCreate(BaseModel):
    title: str
    description: str
    company: str


# response
class JobResponse(BaseModel):
    id: UUID
    title: str
    description: str
    company: str
    recruiter_id: UUID

    class Config:
        from_attributes = True
