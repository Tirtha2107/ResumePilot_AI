def technical():
    import os
    import json
    import re
    import streamlit as st
    from dotenv import load_dotenv
    from google import genai


    load_dotenv()

    API_KEY = os.getenv("GEMINI_API_KEY")

    if not API_KEY:
        st.error("GEMINI_API_KEY not found in .env file.")
        st.stop()

    client = genai.Client(api_key=API_KEY)


    st.header("Technical Round")

    st.markdown(
        """
        Practice important technical interview questions
        using AI-generated questions based on your selected technology.
        """
    )


    st.markdown(
        """
        <style>

        /* Main buttons */

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
        }

        /* Selectbox */

        div[data-baseweb="select"] > div {
            border-radius: 10px;
        }

        /* Expander */

        div[data-testid="stExpander"] {
            border-radius: 12px;
            border: 1px solid #E5E7EB;
        }

        </style>
        """,
        unsafe_allow_html=True
    )



    st.markdown("Select Technology")

    technologies = [
        "Python",
        "Java",
        "C++",
        "Data Structures & Algorithms",
        "DBMS",
        "SQL",
        "Operating System",
        "Computer Networks",
        "Object Oriented Programming"
    ]

    selected_technology = st.selectbox(
        "Choose a technology",
        technologies,
        label_visibility="collapsed"
    )


    st.markdown("Select Difficulty")

    difficulty = st.selectbox(
        "Choose difficulty",
        [
            "Mixed",
            "Easy",
            "Medium",
            "Hard"
        ],
        label_visibility="collapsed"
    )

    if st.button(
        "Generate 10 Interview Questions",
        use_container_width=True
    ):

        with st.spinner(
            f"Generating {selected_technology} interview questions..."
        ):

            prompt = f"""
    You are an expert technical interviewer.

    Generate exactly 10 important technical interview questions
    for a diploma or engineering student preparing for placements.

    Technology:
    {selected_technology}

    Difficulty:
    {difficulty}

    The questions must be useful for real technical interviews.

    Include a mixture of:

    1. Conceptual questions
    2. Logic-based questions
    3. Coding questions
    4. Output prediction questions
    5. Practical/application questions

    For coding questions:
    - Include a short code example when appropriate.
    - Keep the code easy to read.

    For output questions:
    - Include the code.
    - Ask what the output will be.

    For every question provide:

    - question
    - type
    - difficulty
    - answer
    - explanation

    IMPORTANT RULES:

    - Generate exactly 10 questions.
    - Do not repeat questions.
    - Keep answers technically correct.
    - Questions should be suitable for diploma/engineering students.
    - Include important interview questions.
    - Do not use HTML.
    - Do not use <div>.
    - Do not use HTML tags.
    - Do not return Markdown code fences around the JSON.
    - Return ONLY valid JSON.

    Use exactly this structure:

    {{
        "questions": [
            {{
                "question": "Question text",
                "type": "Concept",
                "difficulty": "Easy",
                "answer": "Correct answer",
                "explanation": "Clear explanation"
            }}
        ]
    }}
    """

            try:

                response = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=prompt
                )

                result = response.text.strip()


                result = result.replace("```json", "")
                result = result.replace("```", "")
                result = result.strip()

                # Find JSON if AI adds extra text
                start = result.find("{")
                end = result.rfind("}")

                if start != -1 and end != -1:
                    result = result[start:end + 1]

                data = json.loads(result)

                questions = data.get("questions", [])

                if len(questions) == 0:
                    st.error("No questions were generated.")
                    st.stop()

                # Save questions
                st.session_state.technical_questions = questions
                st.session_state.technical_topic = selected_technology

                st.success(
                    f"10 {selected_technology} questions generated!"
                )

            except json.JSONDecodeError:

                st.error(
                    "AI returned an invalid response. Please try again."
                )

            except Exception as e:

                st.error(
                    f"Error generating questions: {str(e)}"
                )


   

    if "technical_questions" in st.session_state:

        questions = st.session_state.technical_questions
        topic = st.session_state.technical_topic

        st.divider()

        st.markdown(
            f"Top 10 {topic} Interview Questions"
        )

        st.caption(
            "Click on each question to view the answer and explanation."
        )

        

        for i, q in enumerate(questions, start=1):

            question_text = q.get(
                "question",
                "Question unavailable"
            )

            question_type = q.get(
                "type",
                "Technical"
            )

            question_difficulty = q.get(
                "difficulty",
                "Medium"
            )

            answer = q.get(
                "answer",
                "Answer unavailable"
            )

            explanation = q.get(
                "explanation",
                "Explanation unavailable"
            )

        

            question_text = re.sub(
                r"<[^>]+>",
                "",
                str(question_text)
            )

            answer = re.sub(
                r"<[^>]+>",
                "",
                str(answer)
            )

            explanation = re.sub(
                r"<[^>]+>",
                "",
                str(explanation)
            )

            # Remove unnecessary code fences
            question_text = question_text.replace(
                "```",
                ""
            )

            answer = answer.replace(
                "```",
                ""
            )

            explanation = explanation.replace(
                "```",
                ""
            )

           

            st.markdown(
                f"### 🔹 Question {i}"
            )


            st.markdown(
                f"**{question_text}**"
            )


            col1, col2 = st.columns(2)

            with col1:
                st.caption(
                    f"Type: {question_type}"
                )

            with col2:
                st.caption(
                    f"Difficulty: {question_difficulty}"
                )

            

            with st.expander("View Answer & Explanation"):

                st.markdown("Answer")

                st.markdown(answer)

                st.markdown("Explanation")

                st.markdown(explanation)

            st.divider()




    if "technical_questions" in st.session_state:

        if st.button(
            "Generate New Questions",
            use_container_width=True
        ):

            del st.session_state.technical_questions

            if "technical_topic" in st.session_state:
                del st.session_state.technical_topic

            st.rerun()