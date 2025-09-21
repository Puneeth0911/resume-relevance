# app/scoring.py
from sentence_transformers import SentenceTransformer, util
from rapidfuzz import fuzz
import numpy as np

# Load once (in app startup)
MODEL_NAME = "all-MiniLM-L6-v2"
embed_model = SentenceTransformer(MODEL_NAME)

def embed_text(text):
    return embed_model.encode(text, convert_to_tensor=True)

def cosine_score(emb1, emb2):
    return float(util.cos_sim(emb1, emb2).cpu().numpy().item())

# Simple skill extraction: match from a curated skill list
CURATED_SKILLS = {"python","java","c++","machine learning","deep learning","nlp","sql","react","nodejs","aws","docker"}

def extract_skills_from_text(text):
    text_low = text.lower()
    found = [s for s in CURATED_SKILLS if s in text_low]
    return set(found)

def hard_skill_score(jd_skills, resume_skills):
    if not jd_skills:
        return 0.0
    matched = jd_skills.intersection(resume_skills)
    return len(matched) / len(jd_skills)  # 0..1

def fuzzy_keyword_score(jd_text, resume_text):
    # rough measure: partial ratio between JD and resume combined text
    return fuzz.partial_ratio(jd_text, resume_text) / 100.0  # 0..1

def final_score(jd_text, resume_text, jd_skills=None):
    resume_skills = extract_skills_from_text(resume_text)
    if jd_skills is None:
        jd_skills = extract_skills_from_text(jd_text)

    hard = hard_skill_score(set(jd_skills), resume_skills)  # 0..1
    emb1 = embed_text(jd_text)
    emb2 = embed_text(resume_text)
    soft = (cosine_score(emb1, emb2) + 1) / 2  # cosine might be [-1,1]; normalize to 0..1
    fuzzy = fuzzy_keyword_score(jd_text, resume_text)

    # Weighted sum (tuneable)
    w_hard, w_soft, w_fuzzy = 0.5, 0.4, 0.1
    score = w_hard*hard + w_soft*soft + w_fuzzy*fuzzy
    return float(score*100), resume_skills, {"hard":hard, "soft":soft, "fuzzy":fuzzy}
