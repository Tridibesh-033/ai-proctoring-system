from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.dependencies import get_current_user, candidate_only
from app.services.exam_attempt_service import (
    start_exam_attempt,
    fetch_exam_questions
)

router = APIRouter(prefix="/candidate", tags=["Candidate Exam"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/start-exam/{exam_id}")
def start_exam(
    exam_id: str,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    candidate_only(current_user)

    attempt_id = start_exam_attempt(db, exam_id, current_user.id)
    return {
        "message": "Exam Started successfully",
        "attempt_id": attempt_id
    }


@router.get("/exam/{exam_id}/questions")
def get_exam_questions(
    exam_id: str,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    candidate_only(current_user)
    
    return fetch_exam_questions(db, exam_id, current_user.id)

