from app.ai.semantic_matcher import semantic_similarity
from app.ai.tfidf_matcher import tfidf_score
from app.ai.openrouter_scorer import openrouter_resume_score

def final_score(resume_text: str, job_text: str) -> float:
    semantic = semantic_similarity(resume_text, job_text)
    # tfidf = tfidf_score(resume_text, job_text)
    openroter_llm=openrouter_resume_score(resume_text, job_text)


    print("Semantic:", semantic)
    # print("TFIDF:", tfidf)
    print("Openrouter_llm:", openroter_llm)

    final = (
        semantic * 0.40 +
        openroter_llm * 0.60
    )

    return round(min(final, 92), 2)


