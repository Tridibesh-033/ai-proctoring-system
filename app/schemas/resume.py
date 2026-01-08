from pydantic import BaseModel

class ResumeResponse(BaseModel):
    message: str
    file_path: str
