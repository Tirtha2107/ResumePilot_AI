import os
import json
import io
import re

import streamlit as st
from dotenv import load_dotenv
from google import genai


# =========================================================
# GEMINI CONFIGURATION
# =========================================================

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    st.error("GEMINI_API_KEY not found in .env file.")
    st.stop()

client = genai.Client(api_key=API_KEY)

# Keep this as a variable so you can easily change it later.
# Example current model:
MODEL_NAME = "gemini-2.5-flash"


# =========================================================
# MAIN FUNCTION
# =========================================================

def mock():

    # =====================================================
    # CSS
    # =====================================================

    st.markdown("""
    <style>

    .stButton > button {
        background-color: #5B5EF7;
        color: white;
        border: none;
        border-radius: 12px;
        min-height: 48px;
        font-size: 16px;
        font-weight: 600;
    }

    .stButton > button:hover {
        background-color: #4B4EE6;
        color: white;
        box-shadow: 0px 6px 16px rgba(91,94,247,0.30);
    }

    div[data-testid="stAudioInput"] {
        border-radius: 15px;
    }

    div[data-testid="stExpander"] {
        border-radius: 12px;
        border: 1px solid #E5E7EB;
    }

    </style>
    """, unsafe_allow_html=True)


    # =====================================================
    # SESSION STATE
    # =====================================================

    if "mock_started" not in st.session_state:
        st.session_state.mock_started = False

    if "mock_questions" not in st.session_state:
        st.session_state.mock_questions = []

    if "mock_current" not in st.session_state:
        st.session_state.mock_current = 0

    if "mock_results" not in st.session_state:
        st.session_state.mock_results = []

    if "mock_completed" not in st.session_state:
        st.session_state.mock_completed = False

    if "mock_audio_processed" not in st.session_state:
        st.session_state.mock_audio_processed = False


    # =====================================================
    # HEADER
    # =====================================================

    st.header("AI HR Interview")

    st.markdown(
        """
        Practice a real interview with an AI interviewer.

        Speak your answer naturally using your microphone.
        AI will convert your speech into text and evaluate
        your answer.
        """
    )

    st.write("")


    # =====================================================
    # FINAL REPORT
    # =====================================================

    if st.session_state.mock_completed:

        st.markdown("## Mock Interview Completed!")

        results = st.session_state.mock_results

        if results:

            total_score = sum(
                int(result.get("score", 0))
                for result in results
            )

            max_score = len(results) * 10

            percentage = round(
                (total_score / max_score) * 100
            )

            # ---------------------------------------------
            # PERFORMANCE LEVEL
            # ---------------------------------------------

            if percentage >= 80:
                level = "Excellent"

            elif percentage >= 60:
                level = "Good"

            elif percentage >= 40:
                level = "Needs Improvement"

            else:
                level = "Needs More Practice"


            # ---------------------------------------------
            # SUMMARY
            # ---------------------------------------------

            st.markdown("Interview Performance")

            col1, col2, col3 = st.columns(3)

            with col1:
                st.metric(
                    "Overall Score",
                    f"{total_score}/{max_score}"
                )

            with col2:
                st.metric(
                    "Percentage",
                    f"{percentage}%"
                )

            with col3:
                st.metric(
                    "Performance",
                    level
                )

            st.progress(
                percentage / 100
            )


            # ---------------------------------------------
            # QUESTION RESULTS
            # ---------------------------------------------

            st.markdown("Question-wise Performance")

            for i, result in enumerate(results, start=1):

                question = result.get(
                    "question",
                    "Question unavailable"
                )

                user_answer = result.get(
                    "user_answer",
                    "No answer"
                )

                score = int(
                    result.get(
                        "score",
                        0
                    )
                )

                feedback = result.get(
                    "feedback",
                    ""
                )

                strengths = result.get(
                    "strengths",
                    []
                )

                improvements = result.get(
                    "improvements",
                    []
                )

                with st.container(border=True):

                    st.markdown(
                        f"### Question {i}"
                    )

                    st.markdown(
                        f"**{question}**"
                    )

                    st.markdown(
                        f"Score: {score}/10"
                    )

                    with st.expander(
                        "View Your Answer"
                    ):

                        st.write(
                            user_answer
                        )

                    st.markdown(
                        "AI Feedback"
                    )

                    st.write(
                        feedback
                    )

                    if strengths:

                        st.markdown(
                            "What You Did Well"
                        )

                        for item in strengths:

                            st.markdown(
                                f"- {item}"
                            )

                    if improvements:

                        st.markdown(
                            "Areas to Improve"
                        )

                        for item in improvements:

                            st.markdown(
                                f"- {item}"
                            )


            # ---------------------------------------------
            # FINAL RECOMMENDATION
            # ---------------------------------------------

            st.markdown("AI Recommendation")

            if percentage >= 80:

                st.success(
                    """
                    Excellent interview performance!

                    You demonstrate good technical knowledge
                    and interview readiness. Continue practicing
                    advanced and project-based questions.
                    """
                )

            elif percentage >= 60:

                st.info(
                    """
                    Good performance!

                    Your fundamentals are developing well.
                    Focus on giving more structured and confident
                    answers.
                    """
                )

            else:

                st.warning(
                    """
                    You need more practice.

                    Focus on technical fundamentals, answer
                    structure and speaking clearly.
                    """
                )


        st.write("")

        # ---------------------------------------------
        # NEW INTERVIEW
        # ---------------------------------------------

        if st.button(
            "Start New Mock Interview",
            use_container_width=True
        ):

            st.session_state.mock_started = False
            st.session_state.mock_questions = []
            st.session_state.mock_current = 0
            st.session_state.mock_results = []
            st.session_state.mock_completed = False
            st.session_state.mock_audio_processed = False

            st.rerun()

        return


    # =====================================================
    # INTERVIEW SETUP
    # =====================================================

    if not st.session_state.mock_started:

        st.markdown("Interview Setup")

        with st.container(border=True):

            st.markdown("Interview Type")

            interview_type = st.selectbox(
                "Interview Type",
                [
                    "HR"
                ],
                label_visibility="collapsed"
            )


            st.markdown("Difficulty")

            difficulty = st.selectbox(
                "Difficulty",
                [
                    "Mixed",
                    "Easy",
                    "Medium",
                    "Hard"
                ],
                label_visibility="collapsed"
            )


            st.markdown("Number of Questions")

            number_questions = st.selectbox(
                "Number of Questions",
                [
                    1,
                    3,
                    5,
                    10
                ],
                index=1,
                label_visibility="collapsed"
            )


        st.write("")

       

        st.markdown("Mock Interview Features")

        col1, col2, col3 = st.columns(3)

        with col1:

            st.markdown("""
            **Voice Answer**

            Speak your answer instead
            of typing it.
            """)

        with col2:

            st.markdown("""
            **AI Evaluation**

            AI evaluates your answer
            and gives feedback.
            """)

        with col3:

            st.markdown("""

            **Performance Report**

            Get your score and areas
            for improvement.
            """)


        st.write("")



        if st.button(
            "Start Mock Interview",
            use_container_width=True
        ):

            with st.spinner(
                "AI is preparing your interview..."
            ):

                prompt = f"""
You are a professional placement interviewer.

Create a realistic mock interview.

Interview Type:
{interview_type}

Difficulty:
{difficulty}

Number of Questions:
{number_questions}

Generate exactly {number_questions} questions.

If the interview is Technical:
- Include programming concepts
- Logic questions
- Coding questions
- Output questions
- Practical technical questions

If the interview is HR:
- Include common HR questions
- Behavioral questions
- Situational questions
- Career questions

If the interview is Mixed:
- Combine technical and HR questions.

The questions must be suitable for
diploma and engineering students.

Make the questions realistic for
college placement interviews.

Do not repeat questions.

Do not use HTML.

Return ONLY valid JSON.

Use exactly this format:

{{
    "questions": [
        {{
            "question": "Question text",
            "category": "Technical or HR",
            "difficulty": "Easy, Medium or Hard"
        }}
    ]
}}
"""

                try:

                    response = client.models.generate_content(
                        model=MODEL_NAME,
                        contents=prompt
                    )

                    result = response.text.strip()

                    # Remove markdown code fences
                    result = result.replace(
                        "```json",
                        ""
                    )

                    result = result.replace(
                        "```",
                        ""
                    )

                    # Find JSON
                    start = result.find("{")
                    end = result.rfind("}")

                    if start != -1 and end != -1:

                        result = result[
                            start:end + 1
                        ]

                    data = json.loads(result)

                    questions = data.get(
                        "questions",
                        []
                    )

                    if len(questions) < number_questions:

                        st.error(
                            "AI did not generate enough questions."
                        )

                        return


                    st.session_state.mock_questions = (
                        questions[:number_questions]
                    )

                    st.session_state.mock_current = 0
                    st.session_state.mock_results = []
                    st.session_state.mock_started = True
                    st.session_state.mock_completed = False
                    st.session_state.mock_audio_processed = False

                    st.rerun()


                except json.JSONDecodeError:

                    st.error(
                        "AI returned an invalid response."
                    )

                except Exception as e:

                    if "429" in str(e):

                        st.error(
                            """
                            Gemini API quota exceeded.

                            Please wait and try again later.
                            """
                        )

                    else:

                        st.error(
                            f"Error generating interview: {str(e)}"
                        )

        return




    questions = st.session_state.mock_questions

    current = st.session_state.mock_current

    total_questions = len(questions)



    if current >= total_questions:

        st.session_state.mock_completed = True

        st.rerun()



    question_data = questions[current]

    question = question_data.get(
        "question",
        "Question unavailable"
    )

    category = question_data.get(
        "category",
        "Technical"
    )

    difficulty = question_data.get(
        "difficulty",
        "Medium"
    )


    st.markdown(
        f"Question {current + 1} of {total_questions}"
    )

    st.progress(
        (current + 1) / total_questions
    )




    with st.container(border=True):

        st.markdown(
            "AI Interviewer"
        )

        st.markdown(
            f"## {question}"
        )

        col1, col2 = st.columns(2)

        with col1:

            st.caption(
                f"Category: {category}"
            )

        with col2:

            st.caption(
                f"Difficulty: {difficulty}"
            )


    st.write("")


  

    st.markdown(" Your Answer")

    st.info(
        "Speak naturally for about 30–60 seconds."
    )

    audio = st.audio_input(
        "Click here to record your answer",
        sample_rate=16000,
        key=f"mock_audio_{current}"
    )


    if audio:

        st.audio(
            audio,
            format="audio/wav"
        )

        st.write("")

        if st.button(
            "Submit Voice Answer",
            use_container_width=True,
            key=f"submit_audio_{current}"
        ):

            with st.spinner(
                "Listening and evaluating your answer..."
            ):

                try:

                    # Convert Streamlit UploadedFile
                    # to seekable BytesIO
                

                    audio_bytes = audio.getvalue()

                    audio_file = io.BytesIO(
                        audio_bytes
                    )


                    audio_file = io.BytesIO(audio_bytes)

                    audio_file.name = f"mock_answer_{current}.wav"

                    uploaded_audio = client.files.upload(
                        file=audio_file,
                        config={
                            "mime_type": "audio/wav"
                        }
                    )
                  

                    evaluation_prompt = f"""
You are an expert placement interviewer.

The student was asked:

"{question}"

Interview category:
{category}

Difficulty:
{difficulty}

The attached audio contains the student's spoken answer.

Your job:

1. Transcribe the student's speech accurately.
2. Evaluate the answer.
3. Give a score from 0 to 10.

Evaluate based on:

- Correctness
- Relevance
- Clarity
- Completeness
- Interview quality

IMPORTANT:

- Do not judge the student's accent.
- Do not penalize normal pauses or filler words heavily.
- Focus mainly on the CONTENT of the answer.
- A partially correct answer should receive partial marks.
- Keep feedback useful for a student.

Return ONLY valid JSON.

Use exactly this format:

{{
    "transcript": "Full transcription of student's answer",
    "score": 8,
    "feedback": "Overall evaluation",
    "strengths": [
        "Strength 1",
        "Strength 2"
    ],
    "improvements": [
        "Improvement 1",
        "Improvement 2"
    ]
}}
"""

                    response = client.models.generate_content(
                        model=MODEL_NAME,
                        contents=[
                            evaluation_prompt,
                            uploaded_audio
                        ]
                    )

                    result = response.text.strip()

                   

                    result = result.replace(
                        "```json",
                        ""
                    )

                    result = result.replace(
                        "```",
                        ""
                    )

                    start = result.find("{")
                    end = result.rfind("}")

                    if start != -1 and end != -1:

                        result = result[
                            start:end + 1
                        ]

                    evaluation = json.loads(result)


                   

                    evaluation["question"] = question

                    evaluation["category"] = category

                    evaluation["user_answer"] = evaluation.get(
                        "transcript",
                        "Could not transcribe answer."
                    )

                    st.session_state.mock_results.append(
                        evaluation
                    )

                    st.session_state.mock_audio_processed = True


             

                    st.success(
                        "Your answer has been analyzed!"
                    )

                    st.markdown(
                        "Your Transcribed Answer"
                    )

                    st.write(
                        evaluation.get(
                            "transcript",
                            "No transcription available."
                        )
                    )


                 
                    score = int(
                        evaluation.get(
                            "score",
                            0
                        )
                    )

                    st.markdown(
                        "AI Evaluation"
                    )

                    if score >= 8:

                        st.success(
                            f"Score: {score}/10"
                        )

                    elif score >= 5:

                        st.info(
                            f"Score: {score}/10"
                        )

                    else:

                        st.warning(
                            f"Score: {score}/10"
                        )


             

                    st.markdown(
                        "Feedback"
                    )

                    st.write(
                        evaluation.get(
                            "feedback",
                            ""
                        )
                    )


                    strengths = evaluation.get(
                        "strengths",
                        []
                    )

                    if strengths:

                        st.markdown(
                            "What You Did Well"
                        )

                        for item in strengths:

                            st.markdown(
                                f"- {item}"
                            )


                    improvements = evaluation.get(
                        "improvements",
                        []
                    )

                    if improvements:

                        st.markdown(
                            "Improve"
                        )

                        for item in improvements:

                            st.markdown(
                                f"- {item}"
                            )


                    st.write("")


                except json.JSONDecodeError:

                    st.error(
                        """
                        AI returned an invalid evaluation.
                        Please try recording the answer again.
                        """
                    )

                except Exception as e:

                    if "429" in str(e):

                        st.error(
                            """
                            Gemini API quota exceeded.

                            Please wait and try again later.
                            """
                        )

                    else:

                        st.error(
                            f"Error processing audio: {str(e)}"
                        )

    if (
        st.session_state.mock_audio_processed
        and
        len(st.session_state.mock_results)
        > current
    ):

        st.divider()

        if current + 1 < total_questions:

            if st.button(
                "Next Question",
                use_container_width=True,
                key=f"next_{current}"
            ):

                st.session_state.mock_current += 1

                st.session_state.mock_audio_processed = False

                st.rerun()

        else:

            if st.button(
                "Finish Interview",
                use_container_width=True,
                key="finish_mock"
            ):

                st.session_state.mock_completed = True

                st.rerun()
