from pydantic import BaseModel
from typing import List, Optional

class QuestionOut(BaseModel):
    id: str
    question: str
    type: str
    difficulty: str
    options: Optional[list] = None
    tts_audio_url: Optional[str] = None

class ExamQuestionsResponse(BaseModel):
    mcq: List[QuestionOut]
    coding: List[QuestionOut]
    audio: List[QuestionOut]
    video: List[QuestionOut]
