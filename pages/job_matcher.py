def job_matcher():
    import streamlit as st
    import json
    import os
    import re
    import hashlib

    from dotenv import load_dotenv
    from google import genai
    from google.genai import types

    from db_config import get_connection
    

    st.set_page_config(
        page_title="Job Matcher",
        layout="wide"
    )

    

    st.markdown("""
    <style>

    # .stApp {
    #     background-color: #F5F7FB;
    # }

    # .block-container {
    #     padding-top: 2rem;
    #     padding-bottom: 3rem;
    # }

    /* Main headings */

    h1 {
        color: #121F39 !important;
        font-weight: 750 !important;
    }

    h2 {
        color: #121F39 !important;
        font-weight: 700 !important;
    }

    h3 {
        color: #121F39 !important;
        font-weight: 650 !important;
    }

    /* Buttons */

    .stButton > button {
        background-color: #5B5EF7;
        color: white;
        border: none;
        border-radius: 9px;
        font-weight: 600;
    }

    .stButton > button:hover {
        background-color: #4A4CE5;
        color: white;
        border: none;
    }

    /* Progress */

    .stProgress > div > div > div > div {
        background-color: #5B5EF7;
    }

    /* Metrics */

    [data-testid="stMetric"] {
        background-color: #F8F9FF;
        border: 1px solid #E0E2FF;
        padding: 12px;
        border-radius: 12px;
    }

    /* Alerts */

    [data-testid="stAlert"] {
        border-radius: 10px;
    }

    </style>
    """, unsafe_allow_html=True)

   
    st.markdown("""
                <h1 style="
                    font-size: 42px;
                    font-weight: 750;
                    color: #121F39;
                    margin-bottom: 5px;
                ">
                    Job <span style="color:#5B5EF7;">Matcher</span>
                </h1>
    """, unsafe_allow_html=True)

    st.markdown(
        "Find the job roles that best match your **resume, skills, "
        "education and career profile**."
    )

    st.divider()

   

    if "user_email" not in st.session_state:

        st.error("Please login first.")

        st.info(
            "You need to login before using the Job Matcher."
        )

        st.stop()

    email = st.session_state["user_email"]

    

    try:

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT
                full_name,
                qualification,
                branch,
                college,
                passing_year
            FROM users
            WHERE email = ?
        """, (email,))

        user = cursor.fetchone()

        conn.close()

    except Exception as e:

        st.error(
            f"Database error: {e}"
        )

        st.stop()

    

    if user is None:

        st.error(
            "User profile not found."
        )

        st.stop()

    full_name = user[0]
    qualification = user[1]
    branch = user[2]
    college = user[3]
    passing_year = user[4]

    

    candidate_data = st.session_state.get(
        "candidate_data"
    )

    if candidate_data is None:

        st.warning(
            "Please upload your resume first."
        )

        st.info(
            "Go to the **Upload Resume** page and upload "
            "your resume before using Job Matcher."
        )

        st.stop()

    

    resume_text = candidate_data.get(
        "resume_text",
        ""
    )

    resume_filename = candidate_data.get(
        "resume_filename",
        "Resume"
    )

    

    if not resume_text:

        st.error(
            "Resume text could not be found."
        )

        st.stop()

    if not resume_text.strip():

        st.error(
            "Resume is empty."
        )

        st.stop()

   

    st.subheader("Your Profile")

    profile_col1, profile_col2, profile_col3 = st.columns(3)

    with profile_col1:

        st.markdown("**Name**")

        st.write(
            full_name or "Not Available"
        )

        st.markdown("**Qualification**")

        st.write(
            qualification or "Not Available"
        )

    with profile_col2:

        st.markdown("**Branch**")

        st.write(
            branch or "Not Available"
        )

        st.markdown("**College**")

        st.write(
            college or "Not Available"
        )

    with profile_col3:

        st.markdown("**Passing Year**")

        st.write(
            passing_year or "Not Available"
        )

        st.markdown("**Resume**")

        st.write(
            resume_filename
        )

    st.divider()

    
    load_dotenv()

    api_key = os.getenv(
        "GEMINI_API_KEY"
    )

    if not api_key:

        st.error(
            "Gemini API key not found."
        )

        st.info(
            "Please add GEMINI_API_KEY to your .env file."
        )

        st.stop()

    

    try:

        client = genai.Client(
            api_key=api_key
        )

    except Exception as e:

        st.error(
            f"Gemini initialization failed: {e}"
        )

        st.stop()

  

    resume_hash = hashlib.md5(
        resume_text.encode("utf-8")
    ).hexdigest()

    cache_key = (
        f"job_matcher_{email}_{resume_hash}"
    )



    refresh_col1, refresh_col2 = st.columns(
        [5, 1]
    )

    with refresh_col1:

        st.markdown(
            "## Recommended Jobs"
        )

    with refresh_col2:

        if st.button(
            "Refresh",
            use_container_width=True
        ):

            if cache_key in st.session_state:

                del st.session_state[
                    cache_key
                ]

            st.rerun()

   

    if cache_key in st.session_state:

        jobs = st.session_state[
            cache_key
        ]

    else:

    

        resume_for_ai = resume_text[:18000]

     

        prompt = f"""
You are an expert AI Career Advisor and Recruitment Specialist.

Your job is to analyze a candidate's profile and resume and
recommend the 3 most suitable entry-level job roles.

============================================================
CANDIDATE PROFILE
============================================================

Name:
{full_name}

Qualification:
{qualification}

Branch:
{branch}

College:
{college}

Passing Year:
{passing_year}

Resume File:
{resume_filename}

============================================================
RESUME
============================================================

{resume_for_ai}

============================================================
TASK
============================================================

Recommend exactly 3 job roles that are genuinely suitable
for this candidate.

Analyze:

1. Education
2. Branch
3. Programming languages
4. Technical skills
5. Projects
6. Databases
7. Frameworks
8. Tools
9. Certifications
10. Internship or experience
11. Overall career suitability

Do NOT recommend jobs simply because they are popular.

Recommendations must be based primarily on the candidate's
actual resume and profile.

============================================================
MATCH SCORE
============================================================

Give each job a realistic match score between 0 and 100.

90-100 = Excellent match
80-89  = Very good match
70-79  = Good match
60-69  = Moderate match
Below 60 = Weak match

Do not give every job an artificially high score.

============================================================
SALARY
============================================================

Give a realistic estimated entry-level salary range in India.

Example:

₹4-7 LPA

Do not guarantee salary.

============================================================
COMPANIES
============================================================

Suggest companies that commonly hire for similar roles.

Do NOT say that the candidate is guaranteed to get a job
at any listed company.

============================================================
OUTPUT
============================================================

Return ONLY valid JSON.

Use exactly this structure:

{{
    "jobs": [
        {{
            "role": "Python Developer",
            "domain": "Software Development",
            "match": 88,
            "salary": "₹4-7 LPA",
            "experience": "0-1 Years",
            "description": "Develop software and backend applications using Python.",
            "why_match": "The candidate has Python, SQL and software development project experience.",
            "companies": [
                "TCS",
                "Infosys",
                "Accenture"
            ],
            "skills": [
                "Python",
                "SQL",
                "Git",
                "OOP"
            ],
            "missing_skills": [
                "Django",
                "REST API"
            ]
        }}
    ]
}}

============================================================
STRICT RULES
============================================================

1. Return exactly 3 jobs.
2. Match must be an integer from 0 to 100.
3. Companies must be an array of strings.
4. Skills must be an array of strings.
5. Missing skills must be an array of strings.
6. Do not invent skills that are not present in the resume.
7. Keep descriptions concise.
8. Return JSON only.
9. Do not use Markdown.
10. Do not wrap JSON inside ```json.
"""

        

        try:

            with st.spinner(
                "Analyzing your resume and finding the best jobs..."
            ):

                response = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=prompt,
                    config=types.GenerateContentConfig(
                        temperature=0.3,
                        response_mime_type="application/json"
                    )
                )

        except Exception as e:

            error_message = str(e)

            if (
                "429" in error_message
                or
                "RESOURCE_EXHAUSTED" in error_message
            ):

                st.error(
                    "Gemini API quota has been exceeded."
                )

                st.info(
                    "Please wait for the quota to reset "
                    "or use another Gemini API key."
                )

            elif (
                "401" in error_message
                or
                "403" in error_message
            ):

                st.error(
                    "Gemini API key is invalid or unauthorized."
                )

            else:

                st.error(
                    f"Gemini Error: {error_message}"
                )

            st.stop()

        

        if not response:

            st.error(
                "Gemini did not return a response."
            )

            st.stop()

        if not response.text:

            st.error(
                "Gemini returned an empty response."
            )

            st.stop()

        text = response.text.strip()


        if text.startswith("```"):

            text = re.sub(
                r"^```(?:json)?",
                "",
                text,
                flags=re.IGNORECASE
            )

            text = re.sub(
                r"```$",
                "",
                text
            )

            text = text.strip()

   

        try:

            data = json.loads(
                text
            )

        except json.JSONDecodeError:

            # Try extracting JSON object
            json_match = re.search(
                r"\{.*\}",
                text,
                re.DOTALL
            )

            if json_match:

                try:

                    data = json.loads(
                        json_match.group()
                    )

                except json.JSONDecodeError:

                    st.error(
                        "Gemini returned invalid JSON."
                    )

                    st.code(text)

                    st.stop()

            else:

                st.error(
                    "Could not find JSON in Gemini response."
                )

                st.code(text)

                st.stop()

        

        jobs = data.get(
            "jobs",
            []
        )

        if not isinstance(
            jobs,
            list
        ):

            st.error(
                "Invalid job recommendation format."
            )

            st.stop()

        if not jobs:

            st.warning(
                "No suitable job recommendations found."
            )

            st.stop()

       

        cleaned_jobs = []

        for job in jobs[:3]:

            if not isinstance(
                job,
                dict
            ):

                continue

            

            try:

                match = int(
                    job.get(
                        "match",
                        0
                    )
                )

            except:

                match = 0

            match = max(
                0,
                min(
                    100,
                    match
                )
            )

       

            companies = job.get(
                "companies",
                []
            )

            skills = job.get(
                "skills",
                []
            )

            missing_skills = job.get(
                "missing_skills",
                []
            )

            if not isinstance(
                companies,
                list
            ):

                companies = []

            if not isinstance(
                skills,
                list
            ):

                skills = []

            if not isinstance(
                missing_skills,
                list
            ):

                missing_skills = []

            

            cleaned_jobs.append({

                "role": str(
                    job.get(
                        "role",
                        "Unknown Role"
                    )
                ),

                "domain": str(
                    job.get(
                        "domain",
                        "Not Available"
                    )
                ),

                "match": match,

                "salary": str(
                    job.get(
                        "salary",
                        "Not Available"
                    )
                ),

                "experience": str(
                    job.get(
                        "experience",
                        "0-1 Years"
                    )
                ),

                "description": str(
                    job.get(
                        "description",
                        ""
                    )
                ),

                "why_match": str(
                    job.get(
                        "why_match",
                        ""
                    )
                ),

                "companies": [
                    str(company)
                    for company in companies[:5]
                ],

                "skills": [
                    str(skill)
                    for skill in skills[:8]
                ],

                "missing_skills": [
                    str(skill)
                    for skill in missing_skills[:6]
                ]
            })

 

        if not cleaned_jobs:

            st.error(
                "No valid job recommendations were generated."
            )

            st.stop()

      

        cleaned_jobs.sort(
            key=lambda x: x["match"],
            reverse=True
        )


        st.session_state[
            cache_key
        ] = cleaned_jobs

        jobs = cleaned_jobs

    

    for job_index, job in enumerate(jobs):

        role = job.get(
            "role",
            "Unknown Role"
        )

        domain = job.get(
            "domain",
            "Not Available"
        )

        match = job.get(
            "match",
            0
        )

        salary = job.get(
            "salary",
            "Not Available"
        )

        experience = job.get(
            "experience",
            "Not Available"
        )

        description = job.get(
            "description",
            ""
        )

        why_match = job.get(
            "why_match",
            ""
        )

        companies = job.get(
            "companies",
            []
        )

        skills = job.get(
            "skills",
            []
        )

        missing_skills = job.get(
            "missing_skills",
            []
        )

        # ====================================================
        # JOB CARD
        # ====================================================

        with st.container(border=True):

            # ------------------------------------------------
            # JOB TITLE
            # ------------------------------------------------

            title_col, match_col = st.columns(
                [4, 1]
            )

            with title_col:

                st.subheader(
                    f"{role}"
                )

                st.caption(
                    f"{domain}"
                )

            with match_col:

                st.metric(
                    "Match",
                    f"{match}%"
                )

            

            st.progress(
                match / 100
            )

           

            st.markdown(
                "Job Information"
            )

            info1, info2, info3 = st.columns(3)

            with info1:

                st.markdown(
                    "**Salary**"
                )

                st.success(
                    salary
                )

            with info2:

                st.markdown(
                    "**Experience**"
                )

                st.info(
                    experience
                )

            with info3:

                st.markdown(
                    "**Domain**"
                )

                st.write(
                    domain
                )

          

            if description:

                st.markdown(
                    "Job Description"
                )

                st.write(
                    description
                )

       

            if why_match:

                st.markdown(
                    "Why This Job Matches You"
                )

                st.info(
                    why_match
                )

           

            if companies:

                st.markdown(
                    "Top Companies"
                )

                company_cols = st.columns(
                    min(
                        3,
                        len(companies)
                    )
                )

                for i, company in enumerate(
                    companies
                ):

                    with company_cols[
                        i % len(company_cols)
                    ]:

                        st.success(
                            company
                        )

            

            if skills:

                st.markdown(
                    "### Key Skills"
                )

                skill_cols = st.columns(
                    min(
                        4,
                        len(skills)
                    )
                )

                for i, skill in enumerate(
                    skills
                ):

                    with skill_cols[
                        i % len(skill_cols)
                    ]:

                        st.button(
                            f"✓ {skill}",
                            disabled=True,
                            key=(
                                f"skill_"
                                f"{job_index}_"
                                f"{i}"
                            )
                        )

            

            if missing_skills:

                st.markdown(
                    " Skills to Improve"
                )

                missing_cols = st.columns(
                    min(
                        3,
                        len(missing_skills)
                    )
                )

                for i, skill in enumerate(
                    missing_skills
                ):

                    with missing_cols[
                        i % len(missing_cols)
                    ]:

                        st.warning(
                            f"{skill}"
                        )

            

            with st.expander(
                "View Complete Details"
            ):

                st.markdown(
                    f"**Job Role:** {role}"
                )

                st.markdown(
                    f"**Domain:** {domain}"
                )

                st.markdown(
                    f"**Match:** {match}%"
                )

                st.markdown(
                    f"**Salary:** {salary}"
                )

                st.markdown(
                    f"**Experience:** {experience}"
                )

                if description:

                    st.markdown(
                        "#### Job Description"
                    )

                    st.write(
                        description
                    )

                if why_match:

                    st.markdown(
                        "#### Why You Match"
                    )

                    st.write(
                        why_match
                    )

                if companies:

                    st.markdown(
                        "#### Companies"
                    )

                    st.write(
                        ", ".join(companies)
                    )

                if skills:

                    st.markdown(
                        "#### Skills"
                    )

                    st.write(
                        ", ".join(skills)
                    )

                if missing_skills:

                    st.markdown(
                        "#### Skills to Improve"
                    )

                    st.write(
                        ", ".join(missing_skills)
                    )

           

            st.divider()


    st.markdown(
        "Keep Learning. Keep Improving."
    )

    st.caption(
        "Your dream job is closer than you think!"
    )