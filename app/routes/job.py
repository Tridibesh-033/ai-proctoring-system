from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.job import Job
from app.schemas.job import JobCreate
from app.dependencies import get_current_user, recruiter_only
from app.models.user import User


router = APIRouter(prefix="/jobs", tags=["Jobs"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/create")
def create_job(
    job: JobCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    recruiter_only(current_user)

    new_job = Job(
        title=job.title,
        description=job.description,
        company=job.company,
        recruiter_id=current_user.id
    )
    db.add(new_job)
    db.commit()
    db.refresh(new_job)

    return new_job

@router.get("/")
def list_jobs(db: Session = Depends(get_db)):
    return db.query(Job).all()
