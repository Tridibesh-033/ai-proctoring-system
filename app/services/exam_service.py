from app.models.exam import Exam
from app.models.exam_question import ExamQuestion
from app.ai.question_generator import generate_questions


def create_exam(db, job, recruiter_id, config):
    exam = Exam(job_id=job.id, created_by=recruiter_id)
    db.add(exam)
    db.commit()
    db.refresh(exam)

    questions = generate_questions(job.description, config)

    for q in questions:
        db.add(
            ExamQuestion(
                exam_id=exam.id,
                question=q["question"],
                type=q["type"],
                difficulty=q["difficulty"],
                options=q.get("options") if q["type"] == "mcq" else None,
                correct_answer=q.get("correct_answer") if q["type"] == "mcq" or "coding" else None,
            )
        )

    db.commit()
    return exam.id
