def AI():
    import streamlit as st
    from dotenv import load_dotenv
    from google import genai
    import os

    # ---------------- PAGE ----------------

    

    # ---------------- LOAD API KEY ----------------

    load_dotenv()

    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        st.error("GEMINI_API_KEY not found in .env file")
        st.stop()

    client = genai.Client(api_key=api_key)

    # ---------------- CSS ----------------

    st.markdown("""
    <style>

    .title{
        text-align:center;
        font-size:36px;
        font-weight:bold;
        color:black;
    }

    .subtitle{
        text-align:center;
        color:gray;
        margin-bottom:25px;
    }

    </style>
    """, unsafe_allow_html=True)

    # ---------------- HEADER ----------------

    # st.markdown(
    #     "<div class='title'>Interview Preparation Bot</div>",
    #     unsafe_allow_html=True
    # )
    st.markdown("""
            <h1 style="
                font-size: 42px;
                font-weight: 750;
                color: #121F39;
                margin-bottom: 5px;
            ">
                Interview <span style="color:#5B5EF7;">Preparation Bot</span>
            </h1>
            """, unsafe_allow_html=True)
    st.markdown(
        "<div class='subtitle'>Your Personal AI Interview Coach</div>",
        unsafe_allow_html=True
    )

    st.divider()

    # ---------------- CHAT HISTORY ----------------

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # ---------------- CHAT INPUT ----------------

    question = st.chat_input("Ask your interview question...")

    if question:

        st.session_state.messages.append(
            {
                "role":"user",
                "content":question
            }
        )

        with st.chat_message("user"):
            st.markdown(question)

        with st.chat_message("assistant"):

            with st.spinner("Thinking..."):

                prompt = f"""
    You are an Interview Preparation Bot.

    Only answer interview-related questions.

    You may answer:

    - Python
    - Java
    - C++
    - SQL
    - DBMS
    - OOP
    - AI
    - ML
    - Resume
    - HR Interview
    - Aptitude
    - Communication Skills
    - Mock Interview

    If the user asks anything unrelated, reply:

    "I'm an Interview Preparation Bot, so I can only answer interview-related questions."

    Question:
    {question}

    Always finish with one Interview Tip.
    """

                try:

                    response = client.models.generate_content(
                        model="gemini-2.5-flash",
                        contents=prompt
                    )

                    answer = response.text

                except Exception as e:

                    answer = f" Error: {e}"

                st.markdown(answer)

                st.session_state.messages.append(
                    {
                        "role":"assistant",
                        "content":answer
                    }
                )

    st.divider()

