def map():
    import streamlit as st
    from pathlib import Path

    st.set_page_config(
        page_title="Interview Roadmap",
        layout="wide"
    )

    # ---------------- CSS ----------------
    st.markdown("""
    <style>

    .stApp {
        background: #FFFFFF;
    }

    /* Remove Streamlit top spacing */
    # .block-container {
    #     padding-top: 1rem;
    #     padding-left: 2rem;
    #     padding-right: 2rem;
    # }

    /* Hide image border */
    img {
        border-radius: 12px;
    }

    </style>
    """, unsafe_allow_html=True)


    # ---------------- HEADER ----------------

    st.markdown("""
    <h1 style="
        font-size: 42px;
        font-weight: 750;
        color: #121F39;
        margin-bottom: 5px;
    ">
        Interview <span style="color:#5B5EF7;">Roadmap</span>
    </h1>

    <p style="
        font-size: 19px;
        color: #52617A;
        margin-top: 0px;
        margin-bottom: 25px;
    ">
        Your journey from resume screening to receiving your offer!
    </p>
    """, unsafe_allow_html=True)


    # ---------------- ROADMAP IMAGE ----------------

    image_path = Path("assets/map.png")

    if image_path.exists():

        st.image(
            str(image_path),
            use_container_width=True
        )

    else:

        st.error(
            "Roadmap image not found. "
            "Please place interview_roadmap.png inside the assets folder."
        )