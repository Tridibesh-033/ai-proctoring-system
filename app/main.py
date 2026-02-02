from fastapi import FastAPI
from app.database import Base, engine
from app.routes import user, job, resume, exam,exam_attempt 
from fastapi.staticfiles import StaticFiles

Base.metadata.create_all(bind=engine)

app = FastAPI(title="AI Hiring System")

app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(user.router)
app.include_router(job.router)
app.include_router(resume.router)
app.include_router(exam.router)
app.include_router(exam_attempt.router)

@app.get("/")
def root():
    return {"message": "AI Hiring System Backend Running"}
