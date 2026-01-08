from fastapi import FastAPI
from app.database import Base, engine
from app.routes.user import router as user_router

Base.metadata.create_all(bind=engine)

app = FastAPI(title="AI Hiring System")

app.include_router(user_router)

@app.get("/")
def root():
    return {"message": "AI Hiring System Backend Running"}
