from sentence_transformers import SentenceTransformer, util

model = SentenceTransformer("all-MiniLM-L6-v2")

def semantic_similarity(resume_text: str, job_text: str) -> float:
    chunks = resume_text.split("\n")
    chunks = [c for c in chunks if len(c) > 30][:12]

    job_emb = model.encode(job_text, convert_to_tensor=True)
    chunk_embs = model.encode(chunks, convert_to_tensor=True)

    scores = util.cos_sim(job_emb, chunk_embs)
    best = scores.max().item()

    return round(best * 100, 2)
