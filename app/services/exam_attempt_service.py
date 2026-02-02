from sqlalchemy.orm import Session
from app.models.exam_attempt import ExamAttempt
from app.models.exam_question import ExamQuestion
from app.ai.text_to_speech import generate_tts
from app.services.resume_service import validate_candidate_exam_access
from fastapi import HTTPException
from app.models.exam import Exam


def start_exam_attempt(db, exam_id, candidate_id):
    exam = db.query(Exam).filter(Exam.id == exam_id).first()

    if not exam:
        raise HTTPException(status_code=404, detail="Exam not found")

    job_id = exam.job_id 

    validate_candidate_exam_access(db, candidate_id, job_id)

    # re-entry protection
    existing_attempt = validate_exam_reentry(db, exam_id, candidate_id)

    if existing_attempt:
        return existing_attempt.id  # resume attempt

    attempt = ExamAttempt(
        exam_id=exam_id,
        candidate_id=candidate_id,
        status="STARTED"
    )

    db.add(attempt)
    db.commit()
    db.refresh(attempt)

    return attempt.id


def fetch_exam_questions(db: Session, exam_id,candidate_id):
    exam = db.query(Exam).filter(Exam.id == exam_id).first()

    if not exam:
        raise HTTPException(status_code=404, detail="Exam not found")

    job_id = exam.job_id  

    validate_candidate_exam_access(db,candidate_id,job_id)

    attempt = db.query(ExamAttempt).filter(
        ExamAttempt.exam_id == exam_id,
        ExamAttempt.candidate_id == candidate_id
    ).first()

    if not attempt:
        raise HTTPException(
            status_code=403,
            detail="Start exam before accessing questions"
        )

    if attempt.status != "STARTED":
        raise HTTPException(
            status_code=403,
            detail="Exam already completed or expired"
        )

    questions = db.query(ExamQuestion).filter(
        ExamQuestion.exam_id == exam_id
    ).all()

    result = {
        "mcq": [],
        "coding": [],
        "audio": [],
        "video": []
    }

    for q in questions:
        item = {
            "id": str(q.id),
            "question": q.question,
            "type": q.type,
            "difficulty": q.difficulty,
            "options": q.options
        }

        if q.type in ["audio", "video"]:
            item["tts_audio_url"] = generate_tts(q.question)

        result[q.type].append(item)

    return result


def validate_exam_reentry(db, exam_id, candidate_id):
    attempt = db.query(ExamAttempt).filter(
        ExamAttempt.exam_id == exam_id,
        ExamAttempt.candidate_id == candidate_id
    ).first()

    if attempt:
        if attempt.status == "SUBMITTED":
            raise HTTPException(
                status_code=403,
                detail="Exam already submitted. Re-attempt not allowed."
            )

        if attempt.status == "EXPIRED":
            raise HTTPException(
                status_code=403,
                detail="Exam time expired."
            )

        if attempt.status == "STARTED":
            return attempt  # resume same attempt

    return None

