from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import uuid

from app.schemas.exam import QuestionConfig
from app.services.exam_service import create_exam
from app.database import SessionLocal
from app.models.job import Job
from app.dependencies import get_current_user, recruiter_only

router = APIRouter(prefix="/exam", tags=["Exam"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/generate/{job_id}")
def generate_exam(
    job_id: uuid.UUID,
    config: QuestionConfig,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    recruiter_only(current_user)

    job = db.query(Job).filter(Job.id == job_id).first()

    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    # ensure recruiter owns the job
    if job.recruiter_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="You are not authorized to gererate question for this job"
        )

    exam_id = create_exam(db, job, current_user.id, config.dict())

    return {
        "message": "Exam generated",
        "exam_id": exam_id
    }
