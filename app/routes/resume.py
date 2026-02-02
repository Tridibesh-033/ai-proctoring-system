from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.resume import Resume
from app.models.job import Job
from app.dependencies import get_current_user, candidate_only, recruiter_only
from app.models.user import User
from app.ai.text_utils import extract_text, clean_text
from app.ai.scorer import final_score
import os
import shutil
import uuid

router = APIRouter(prefix="/resume", tags=["Resume"])

UPLOAD_DIR = "app/uploads/resumes"
os.makedirs(UPLOAD_DIR, exist_ok=True)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/upload/{job_id}")
def upload_resume(
    job_id: uuid.UUID,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    
    candidate_only(current_user)

    # only pdf 
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF resumes are allowed")

    # job validation
    job = db.query(Job).filter(Job.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    # duplicate upload
    
    # existing = (
    #     db.query(Resume)
    #     .filter(
    #         Resume.user_id == current_user.id,
    #         Resume.job_id == job_id
    #     )
    #     .first()
    # )
    # if existing:
    #     raise HTTPException(
    #         status_code=400,
    #         detail="Resume already uploaded for this job"
    #     )

    filename = f"{uuid.uuid4()}_{file.filename}"
    file_path = os.path.join(UPLOAD_DIR, filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # ai processing
    raw_resume = extract_text(file_path)
    resume_text = clean_text(raw_resume)
    job_text = clean_text(job.description)
    
    score = float(final_score(resume_text, job_text))

    resume = Resume(
        user_id=current_user.id,
        job_id=job_id,
        file_path=file_path,
        score=score
    )

    db.add(resume)
    db.commit()
    db.refresh(resume)

    return {
        "message": "Resume uploaded & scored",
        "resume_id": str(resume.id),
        "score": score
    }


# ranked candidate based on their score
@router.get("/ranked/{job_id}")
def ranked_candidates(
    job_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    
    recruiter_only(current_user)

    job = db.query(Job).filter(Job.id == job_id).first()

    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    # ensure recruiter owns the job
    if job.recruiter_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="You are not authorized to see ranked candidate based on their score for this job"
        )

    resumes = (
        db.query(Resume)
        .filter(Resume.job_id == job_id)
        .order_by(Resume.score.desc())
        .all()
    )

    return [
        {
            "candidate_id": r.user_id,
            "resume_id": r.id,
            "score": r.score,
            "status": r.status
        }
        for r in resumes
    ]

# candidate shorlisting based on their score
@router.post("/shortlist/{job_id}")
def shortlist_candidates(
    job_id: uuid.UUID,
    cutoff: float = 60.0,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    recruiter_only(current_user)

    job = db.query(Job).filter(Job.id == job_id).first()

    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    # ensure recruiter owns the job
    if job.recruiter_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="You are not authorized to shortlist candidate for this job"
        )

    resumes = (
        db.query(Resume)
        .filter(Resume.job_id == job_id)
        .all()
    )

    if not resumes:
        raise HTTPException(status_code=404, detail="No resumes found")
    
    shortlisted = []
    rejected = []

    for r in resumes:
        # do not override final decisions
        if r.status in ["shortlisted", "rejected"]:
            continue

        if r.score >= cutoff:
            r.status = "shortlisted"
            shortlisted.append(r.user_id)
        else:
            r.status = "rejected"
            rejected.append(r.user_id)

    db.commit()

    return {
        "job_id": str(job_id),
        "cutoff": cutoff,
        "shortlisted_count": len(shortlisted),
        "rejected_count": len(rejected),
        "shortlisted_candidates": shortlisted
    }
