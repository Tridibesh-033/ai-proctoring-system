from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def tfidf_score(resume_text: str, job_text: str) -> float:
    resume_lines = resume_text.split("\n")
    resume_lines = [l for l in resume_lines if len(l) > 40][:10]

    texts = resume_lines + [job_text]

    vectorizer = TfidfVectorizer(
        stop_words="english",
        ngram_range=(1, 2),
        max_features=2000
    )

    vectors = vectorizer.fit_transform(texts)
    scores = cosine_similarity(vectors[-1], vectors[:-1])

    return round(scores.max() * 100, 2)
