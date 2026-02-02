from pydantic import BaseModel

class QuestionConfig(BaseModel):
    mcq: int = 0
    coding: int = 0
    audio: int = 0
    video: int = 0
