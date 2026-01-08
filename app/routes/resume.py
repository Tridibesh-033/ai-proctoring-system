from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID, uuid4
import os
import shutil

from app.database import SessionLocal
from app.models.resume import Resume
from app.dependencies import get_current_user
from app.models.user import User

router = APIRouter(prefix="/resumes", tags=["Resume"])

UPLOAD_DIR = "app/uploads/resumes"
os.makedirs(UPLOAD_DIR, exist_ok=True)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/upload")
def upload_resume(
    job_id: UUID,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Only candidates can upload resumes
    if current_user.role != "candidate":
        raise HTTPException(status_code=403, detail="Only candidates can upload resumes")

    # Generate unique filename
    file_ext = file.filename.split(".")[-1]
    unique_filename = f"{uuid4()}.{file_ext}"
    file_path = os.path.join(UPLOAD_DIR, unique_filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    resume = Resume(
        user_id=current_user.id,
        job_id=job_id,
        file_path=file_path
    )

    db.add(resume)
    db.commit()
    db.refresh(resume)

    return {
        "message": "Resume uploaded successfully",
        "resume_id": resume.id,
        "file_path": file_path
    }
