def resume():
    import os
    import re
    from io import BytesIO
    from typing import List, Tuple
    import streamlit as st
    import numpy as np
    from dotenv import load_dotenv
    from docx import Document
    from google import genai
    from pypdf import PdfReader
    from sentence_transformers import SentenceTransformer
    import json
    import matplotlib.pyplot as plt

    st.markdown("""
    <style>

    /* ===========================
    All Buttons - Blue Theme
    =========================== */

    .stButton > button {
        background-color: #5B5EF7 !important;
        color: white !important;
        border: none !important;
        border-radius: 10px !important;
        font-weight: 600 !important;
        transition: 0.3s;
    }

    .stButton > button:hover {
        background-color: #4548E5 !important;
        color: white !important;
        border: none !important;
    }

    .stButton > button:focus {
        background-color: #5B5EF7 !important;
        color: white !important;
        border: none !important;
        box-shadow: none !important;
    }

    .stButton > button:active {
        background-color: #3B3ED9 !important;
        color: white !important;
    }

    /* Primary Buttons */
    button[kind="primary"] {
        background-color: #5B5EF7 !important;
        color: white !important;
        border: none !important;
    }

    button[kind="primary"]:hover {
        background-color: #4548E5 !important;
        color: white !important;
    }

    /* Download Button */
    .stDownloadButton > button {
        background-color: #5B5EF7 !important;
        color: white !important;
        border: none !important;
    }

    .stDownloadButton > button:hover {
        background-color: #4548E5 !important;
        color: white !important;
    }

    </style>
    """, unsafe_allow_html=True)
    st.markdown("""
    <style>

    .metric-container{
        background:#111827;
        border:2px solid #8B5CF6;      /* Light Purple */
        border-radius:18px;
        padding:25px;
        margin-top:10px;
    }

    .metric-title{
        color:white;
        font-size:28px;
        font-weight:700;
        text-align:center;
        margin-bottom:25px;
    }

    .metric-score{
        color:white;
        font-size:56px;
        font-weight:800;
        text-align:center;
    }

    .metric-status{
        color:white;
        font-size:18px;
        text-align:center;
        margin-top:10px;
    }

    </style>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <style>
    .stProgress > div > div > div > div{
        background:#5B5EF7 !important;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # ---------------
    # --- Load API Key ------------------
    load_dotenv()

    api_key = os.getenv("GEMINI_API_KEY")
    # st.write("API Key Loaded:", api_key[:10] + "..." if api_key else "None")
    

    if not api_key:
        st.error("❌ GEMINI_API_KEY not found in .env file.")
        st.stop()

    # st.set_page_config(
    #     page_title="Resume Analyzer",
    #     layout="wide"
    # )

    # Default settings (No Sidebar)
    model_name = "gemini-2.5-flash"
    top_k = 4

    # ------------------ Embedding Model ------------------
    @st.cache_resource
    def load_embedding_model():
        return SentenceTransformer("all-MiniLM-L6-v2")

    # ------------------ Helper Functions ------------------
    def clean_text(text: str) -> str:
        text = re.sub(r"\s+", " ", text)
        return text.strip()

    def extract_pdf(file_bytes: bytes) -> str:
        reader = PdfReader(BytesIO(file_bytes))
        return "\n".join(page.extract_text() or "" for page in reader.pages)

    def extract_docx(file_bytes: bytes) -> str:
        document = Document(BytesIO(file_bytes))
        return "\n".join(paragraph.text for paragraph in document.paragraphs)

    def extract_text(uploaded_file) -> str:
        file_bytes = uploaded_file.getvalue()
        extension = uploaded_file.name.lower().split(".")[-1]

        if extension == "pdf":
            return clean_text(extract_pdf(file_bytes))
        elif extension == "docx":
            return clean_text(extract_docx(file_bytes))
        elif extension == "txt":
            return clean_text(file_bytes.decode("utf-8", errors="ignore"))
        else:
            raise ValueError("Unsupported file format.")

    def chunk_text(text: str, chunk_size=700, overlap=120):
        words = text.split()
        chunks = []
        start = 0

        while start < len(words):
            end = min(start + chunk_size, len(words))
            chunks.append(" ".join(words[start:end]))

            if end == len(words):
                break

            start = end - overlap

        return chunks

    def retrieve_chunks(
        chunks: List[str],
        query: str,
        model: SentenceTransformer,
        top_k: int = 4,
    ) -> Tuple[List[str], float]:

        chunk_embeddings = model.encode(chunks, normalize_embeddings=True)
        query_embedding = model.encode([query], normalize_embeddings=True)[0]

        scores = chunk_embeddings @ query_embedding

        top_indices = np.argsort(scores)[::-1][:top_k]

        retrieved = [chunks[i] for i in top_indices]
        best_score = float(scores[top_indices[0]])

        return retrieved, best_score

    def score_to_percentage(score):
        score = max(0.0, min(1.0, (score + 1) / 2))
        return round(score * 100)

    def analyze_with_gemini(job_description, context, match_score):

        client = genai.Client(api_key=api_key)

        prompt = f"""
    You are an expert ATS Resume Analyzer and Career Coach.

    JOB DESCRIPTION:
    {job_description}

    RESUME:
    {context}

    Semantic Job Match Score:
    {match_score}/100

    Your task is to evaluate the resume and estimate the following scores realistically.

    Return ONLY valid JSON.

    {{
        "resume_score": 0,
        "ats_score": 0,
        "career_readiness_score": 0,
        "job_match_score": {match_score},

        "matched_skills": [
            "skill1",
            "skill2"
        ],

        "missing_skills": [
            "skill1",
            "skill2"
        ],

        "overview":"2-3 sentence summary of the resume.",

        "overall_assessment":"Detailed assessment.",

        "resume_improvements":[
            "...",
            "...",
            "..."
        ],

        "interview_questions":[
            "...",
            "...",
            "...",
            "...",
            "..."
        ]
    }}

    Rules:

    Resume Score:
    Evaluate overall resume quality.

    ATS Score:
    Evaluate ATS friendliness including keywords, formatting and sections.

    Career Readiness Score:
    Evaluate candidate readiness for the role.

    Job Match Score:
    Use the provided semantic score.

    Return only JSON.
    """

        response = client.models.generate_content(
            model=model_name,
            contents=prompt,
        )

        return response.text

    # ------------------ UI ------------------
    # st.title("Resume Analyzer")
    st.markdown("""
                <h1 style="
                    font-size: 42px;
                    font-weight: 750;
                    color: #121F39;
                    margin-bottom: 5px;
                ">
                    Resume <span style="color:#5B5EF7;">Analyzer</span>
                </h1>
                """, unsafe_allow_html=True)
    st.write("Upload your resume and compare it with a job description.")

    
    resume_file = st.file_uploader(
        "Upload Resume",
        type=["pdf", "docx", "txt"],
        key="resume_upload"
    )

    job_description = st.text_area(
        "Job Description",
        height=220,
        placeholder="Paste the job description here...",
    )

    if st.button("Analyze Resume", type="primary", use_container_width=True):

        if resume_file is None:
            st.error("Please upload a resume.")
            st.stop()

        if not job_description.strip():
            st.error("Please enter the job description.")
            st.stop()

        try:

            # with st.spinner("Reading Resume..."):
            #     resume_text = extract_text(resume_file)
            with st.spinner("Reading Resume..."):
                resume_text = extract_text(resume_file)

                # ==============================
                # Save Resume for Other Pages
                # ==============================
                st.session_state["resume_text"] = resume_text
                st.session_state["resume_filename"] = resume_file.name

                # Optional: Save all candidate data
                st.session_state["candidate_data"] = {
                    "resume_text": resume_text,
                    "resume_filename": resume_file.name
                }

            if len(resume_text.split()) < 20:
                st.error(
                    "Very little text was extracted. Please upload a text-based PDF or DOCX."
                )
                st.stop()

            chunks = chunk_text(resume_text)

            embedding_model = load_embedding_model()

            with st.spinner("Finding relevant resume sections..."):
                retrieved_chunks, similarity = retrieve_chunks(
                    chunks,
                    job_description,
                    embedding_model,
                    top_k=top_k,
                )

            match_score = score_to_percentage(similarity)

            st.subheader("Resume Match Score")
            st.metric("Match", f"{match_score}%")
            context = "\n\n".join(retrieved_chunks)

            with st.spinner("Generating AI Analysis..."):
                analysis = analyze_with_gemini(
                    job_description,
                    context,
                    match_score,
                )

                analysis = analysis.strip()

                if analysis.startswith("```"):
                    analysis = analysis.replace("```json", "").replace("```", "").strip()

                try:
                    data = json.loads(analysis)
                except json.JSONDecodeError:
                    st.error("Gemini returned invalid JSON.")
                    st.code(analysis)
                    st.stop()
                st.subheader("Resume Scores")

             

                def metric_card(title, score):

                    if score >= 85:
                        status = "Excellent"
                    elif score >= 70:
                        status = "Good"
                    else:
                        status = "Needs Improvement"

                    st.markdown(f"""
                <table style="
                width:100%;
                height:180px;
                background:#121F39;
                border:2px solid #8B5CF6;
                border-radius:18px;
                border-collapse:separate;
                text-align:center;
                ">
                <tr>
                    <td style="color:white;font-size:20px;font-weight:700;">
                        {title}
                    </td>
                </tr>

                <tr>
                    <td style="color:white;font-size:45px;font-weight:700;">
                        {score}%
                    </td>
                </tr>

                <tr>
                    <td style="color:#D1D5DB;font-size:16px;">
                        {status}
                    </td>
                </tr>

                </table>
                """, unsafe_allow_html=True)
                
                col1, col2, col3, col4 = st.columns(4)

                with col1:
                    metric_card("Resume Score", data["resume_score"])

                with col2:
                    metric_card("ATS Score", data["ats_score"])

                with col3:
                    metric_card("Hireability", data["career_readiness_score"])

                with col4:
                    metric_card("Job Match", data["job_match_score"])
                st.subheader("Score Summary")

                scores = {
                    "Resume": data["resume_score"],
                    "ATS": data["ats_score"],
                    "Career": data["career_readiness_score"],
                    "Job Match": data["job_match_score"],
                }

         
            st.subheader("Resume Overview")

            st.info(data["overview"])
            st.subheader("Skill Gap Analysis")

            matched = len(data["matched_skills"])
            missing = len(data["missing_skills"])

            fig, ax = plt.subplots(figsize=(5,5))

      
            st.subheader("Matching Skills")

            for skill in data["matched_skills"]:
                # st.success(skill)
                st.markdown(f"• {skill}")
            st.subheader("Missing Skills")

            for skill in data["missing_skills"]:
                st.markdown(f"• {skill}")

            st.subheader("Overall Assessment")

            st.write(data["overall_assessment"])
            st.subheader("Resume Improvements")

            for item in data["resume_improvements"]:
                st.markdown(f"- {item}")

            st.subheader("Interview Questions")

            for i, q in enumerate(data["interview_questions"],1):
                st.markdown(f"**{i}.** {q}")

        
            fig, ax = plt.subplots(figsize=(3, 3))

            ax.pie(
                [matched, missing],
                labels=["Matched", "Missing"],
                autopct="%1.1f%%",
                startangle=90,
                colors=["#5B5EF7", "#121F39"],
                textprops={"color": "white","fontsize": 9}
            )

            ax.axis("equal")
            st.pyplot(fig, use_container_width=False)

        except Exception as e:
            st.error(f"Analysis failed: {e}")
