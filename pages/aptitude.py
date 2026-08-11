import os
import json
import streamlit as st
from dotenv import load_dotenv
from google import genai
def aptitude():

    st.set_page_config(
        page_title="Aptitude Practice",
        layout="wide"
    )

    # CSS


    st.markdown("""
    <style>

    .main-title{
        font-size:38px;
        font-weight:bold;
        color:#1E3A8A;
    }

    .subtitle{
        color:gray;
        font-size:18px;
    }

    div.stButton > button{
        width:100%;
        height:50px;
        border-radius:10px;
        font-weight:bold;
    }

    </style>
    """, unsafe_allow_html=True)

    # LOAD GEMINI API


    # load_dotenv()

    # api_key = os.getenv("GEMINI_API_KEY")

    # if not api_key:
    #     st.error("GEMINI_API_KEY not found in .env")
    #     st.stop()

    load_dotenv()

    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        try:
            api_key = st.secrets["GEMINI_API_KEY"]
        except Exception:
            api_key = None

    if not api_key:
        st.error("GEMINI_API_KEY is not configured.")
        st.stop()

    client = genai.Client(api_key=api_key)

    client = genai.Client(api_key=api_key)

    MODEL_NAME = "gemini-2.5-flash"

    # SESSION STATE
    if "quiz_generated" not in st.session_state:
        st.session_state.quiz_generated = False

    if "quiz_data" not in st.session_state:
        st.session_state.quiz_data = []


    # AI FUNCTION
    

    def generate_quiz(topic, difficulty):

        prompt = f"""
    You are an aptitude interview expert.

    Generate exactly 20 multiple choice questions.

    Topic:
    {topic}

    Difficulty:
    {difficulty}

    Return ONLY JSON.

    Format:

    [
    {{
        "question":"Question",
        "options":[
            "Option A",
            "Option B",
            "Option C",
            "Option D"
        ],
        "answer":"Correct Option",
        "explanation":"Short explanation"
    }}
    ]

    Do not write markdown.

    Do not write anything except JSON.
    """

        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=prompt
        )

        text = response.text.strip()

        if text.startswith("```"):
            text = text.replace("```json", "")
            text = text.replace("```", "")
            text = text.strip()

        return json.loads(text)


    # HEADER
 
    st.header("AI Aptitude Practice")

    st.markdown(
        "<div class='subtitle'>Generate AI-powered aptitude quizzes for placement preparation.</div>",
        unsafe_allow_html=True,
    )

    st.divider()

    # SETTINGS
  
    col1, col2 = st.columns(2)

    with col1:

        topic = st.selectbox(
            "Select Topic",
            [
                "Quantitative Aptitude",
                "Logical Reasoning",
                "Verbal Ability",
                "Mixed Aptitude"
            ]
        )

    with col2:

        difficulty = st.selectbox(
            "Difficulty",
            [
                "Beginner",
                "Intermediate",
                "Advanced"
            ]
        )

 
    # GENERATE QUIZ
   

    if st.button("Generate AI Quiz", use_container_width=True):

        with st.spinner("Generating 20 Questions..."):

            try:

                quiz = generate_quiz(topic, difficulty)

                st.session_state.quiz_data = quiz

                st.session_state.quiz_generated = True

                st.success("Quiz Generated Successfully!")

            except Exception as e:

                st.error(f"Error : {e}")
 
    # DISPLAY QUIZ
    
    if st.session_state.quiz_generated:

        st.divider()
        st.subheader("AI Aptitude Quiz")

        quiz = st.session_state.quiz_data

        # Create answer storage
        if "user_answers" not in st.session_state:
            st.session_state.user_answers = {}

        total_questions = len(quiz)

        answered = len(st.session_state.user_answers)

        st.progress(answered / total_questions if total_questions else 0)

        st.write(f"Answered **{answered} / {total_questions}** Questions")

        st.divider()

        # ----------------------------------------------
        # Display every question
        # ----------------------------------------------

        for i, q in enumerate(quiz):

            st.markdown(f"### Q{i+1}. {q['question']}")

            selected = st.radio(
                "Choose your answer",
                q["options"],
                key=f"question_{i}",
                index=None
            )

            if selected is not None:
                st.session_state.user_answers[i] = selected

            st.write("")

        st.divider()

        # ----------------------------------------------
        # Submit Button
        # ----------------------------------------------

        submit = st.button(
            "Submit Quiz",
            use_container_width=True,
            type="primary"
        )
    # =====================================================
    # SUBMIT QUIZ & EVALUATION
    # =====================================================

    if st.session_state.quiz_generated and submit:

        quiz = st.session_state.quiz_data
        answers = st.session_state.user_answers

        total = len(quiz)
        correct = 0

        st.divider()
        st.header("Quiz Result")

        for i, q in enumerate(quiz):

            user_answer = answers.get(i, "Not Answered")
            correct_answer = q["answer"]

            if user_answer == correct_answer:
                correct += 1

        score = round((correct / total) * 100)

        # Save score for Progress Page
        st.session_state["aptitude_score"] = score
        st.session_state["aptitude_correct"] = correct
        st.session_state["aptitude_total"] = total

        # -------------------------------------
        # Score Card
        # -------------------------------------

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("Score", f"{score}%")

        with col2:
            st.metric("Correct", correct)

        with col3:
            st.metric("Wrong", total - correct)

        st.progress(score / 100)

        # -------------------------------------
        # Grade
        # -------------------------------------

        if score >= 90:
            st.success("Excellent Performance")
        elif score >= 75:
            st.success("Very Good Performance")
        elif score >= 60:
            st.warning("Good. Keep Practicing.")
        else:
            st.error("Practice More.")

        st.divider()

        # -------------------------------------
        # Detailed Report
        # -------------------------------------

        st.subheader("Answer Review")

        for i, q in enumerate(quiz):

            user_answer = answers.get(i, "Not Answered")
            correct_answer = q["answer"]

            with st.expander(f"Question {i+1}"):

                st.markdown(f"**Question:** {q['question']}")

                st.write("**Your Answer:**", user_answer)

                st.write("**Correct Answer:**", correct_answer)

                if user_answer == correct_answer:
                    st.success("Correct")
                else:
                    st.error("Incorrect")

                st.info(q["explanation"])

        st.balloons()

        st.success("Quiz Completed Successfully!")
