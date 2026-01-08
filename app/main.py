from fastapi import FastAPI
from app.database import Base, engine
from app.routes import user, job, resume

Base.metadata.create_all(bind=engine)

app = FastAPI(title="AI Hiring System")

app.include_router(user.router)
app.include_router(job.router)
app.include_router(resume.router)

@app.get("/")
def root():
    return {"message": "AI Hiring System Backend Running"}
