# app/streamlit_app.py
import streamlit as st
import pandas as pd
from parsing import parse_pdf, parse_docx
from scoring import final_score, extract_skills_from_text
from db import init_db, save_result

# -----------------------------
# Page Setup
# -----------------------------
st.set_page_config(page_title="Resume Relevance Checker", layout="wide")
init_db()

st.title("Automated Resume Relevance Check — MVP")

# -----------------------------
# Upload Job Description (JD)
# -----------------------------
st.sidebar.header("1) Upload Job Description (JD)")
jd_file = st.sidebar.file_uploader("Upload JD (txt/pdf/docx)", type=["pdf", "docx", "txt"])

jd_text = ""
if jd_file:
    if jd_file.type == "application/pdf":
        jd_text = parse_pdf(jd_file)
    elif "word" in jd_file.type or jd_file.name.endswith(".docx"):
        jd_text = parse_docx(jd_file)
    else:  # plain text
        jd_text = jd_file.getvalue().decode("utf-8", errors="ignore")

    st.sidebar.success("JD parsed")
    st.subheader("Job Description")
    st.write(jd_text[:2000] + ("..." if len(jd_text) > 2000 else ""))

# -----------------------------
# Upload Resumes
# -----------------------------
st.sidebar.header("2) Upload Resumes")
uploaded = st.sidebar.file_uploader(
    "Resumes (pdf/docx)", 
    accept_multiple_files=True, 
    type=["pdf", "docx"]
)

if uploaded and jd_text:
    results = []
    for idx, f in enumerate(uploaded):
        # Parse each resume
        if f.type == "application/pdf":
            rtext = parse_pdf(f)
        else:
            rtext = parse_docx(f)

        # Score resume
        score, resume_skills, debug = final_score(jd_text, rtext)
        jd_skills = extract_skills_from_text(jd_text)
        missing = jd_skills - resume_skills

        # Verdict thresholds (adjust if needed)
        if score >= 60:
            verdict = "High"
        elif score >= 45:
            verdict = "Medium"
        else:
            verdict = "Low"

        # Save to DB
        save_result(f.name, "Uploaded JD", score, verdict, missing)

        # Collect for display
        results.append({
            "S.No": idx + 1,
            "Filename": f.name,
            "Score": round(score, 2),
            "Verdict": verdict,
            "Missing Skills": ", ".join(missing) if missing else "-"
        })

    # Display results
    st.subheader("Results")
    df = pd.DataFrame(results)
    st.dataframe(df, hide_index=True, use_container_width=True)
    st.success("Evaluation completed ✅")
else:
    if not jd_file:
        st.info("Upload a JD first (sidebar).")
    else:
        st.info("Upload resumes (sidebar).")
