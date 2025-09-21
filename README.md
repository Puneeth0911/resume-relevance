📄 Automated Resume Relevance Check System
🚀 Problem Statement
At Innomatics Research Labs, resume evaluation is currently manual, inconsistent, and time-consuming.
Recruiters spend hours reviewing thousands of resumes against job descriptions (JD), leading to:
Delays in shortlisting candidates
Inconsistent judgments between evaluators
Less time for student guidance & interview prep
👉 We built an AI-powered Resume Relevance Checker that:
Automates resume vs JD evaluation
Generates a Relevance Score (0–100)
Highlights missing skills/projects
Provides a verdict (High / Medium / Low suitability)
Stores results in a dashboard

🛠️ Approach
Workflow

Job Description Upload – Placement team uploads JD (PDF/DOCX/TXT)
Resume Upload – Students upload resumes (PDF/DOCX, multiple files supported)
Parsing – Extracts text using pdfplumber & docx2txt
Relevance Analysis
Hard Match: Skills/keywords check (exact/fuzzy)
Soft Match: Semantic similarity with embeddings (sentence-transformers)
Weighted scoring → Final Score (0–100)

Output
Score, Verdict, Missing Skills
Saved into SQLite database

Dashboard
Streamlit UI with results table
Filter/search capability (extendable)

Tech Stack
Frontend: Streamlit
Backend: Python (FastAPI/Flask ready if extended)
Libraries:
pdfplumber, docx2txt → Resume/JD parsing
sentence-transformers → Embeddings & semantic similarity
rapidfuzz → Fuzzy keyword matching
sqlalchemy & sqlite → Storage
pandas → Dashboard table

⚙️ Installation
Clone the repo and set up environment:
# Clone repository
git clone https://github.com/YOUR_USERNAME/resume-relevance.git
cd resume-relevance
# Create virtual environment
python -m venv venv
# Activate (Windows)
venv\Scripts\activate
# Activate (Mac/Linux)
source venv/bin/activate
# Install dependencies
pip install -r requirements.txt

▶️ Usage
Run the Streamlit app:
cd app
streamlit run streamlit_app.py
Go to http://localhost:8501 in your browser.
Steps in the app:
Upload JD → Choose one JD file (sample_jd_1.pdf or sample_jd_2.pdf)
Upload Resumes → Select multiple resumes (PDF/DOCX)
View Results → Table with Score, Verdict, and Missing Skills

Example Output:
Filename	    Score	Verdict	Missing Skills
resume_1.pdf	82.5	High	   Docker
resume_2.docx	61.2	Medium	NLP, Deep Learning
resume_3.pdf	42.0	Low	    Python, SQL, AWS
