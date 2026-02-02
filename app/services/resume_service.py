from fastapi import HTTPException
from app.models.resume import Resume

def validate_candidate_exam_access(db, user_id, job_id):
    resume = db.query(Resume).filter(
        Resume.user_id == user_id,
        Resume.job_id == job_id
    ).first()

    if not resume:
        raise HTTPException(
            status_code=403,
            detail="You have not applied for this job"
        )

    if resume.status != "shortlisted":
        raise HTTPException(
            status_code=403,
            detail=f"Exam locked. Resume status: {resume.status}"
        )

    return True
