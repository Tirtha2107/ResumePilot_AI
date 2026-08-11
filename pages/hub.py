def hub():
    import streamlit as st

    # ---------------- CUSTOM CSS ----------------
    st.markdown("""
    <style>

    /* Title */
    .title{
        font-size:36px;
        font-weight:700;
        color:#000000;
        margin-bottom:5px;
    }

    .subtitle{
        color:#6B7280;
        font-size:16px;
        margin-bottom:25px;
    }

    /* Small Blue Buttons */
    div.stLinkButton > a{
        background:#5B5EF7 !important;
        color:white !important;
        border:none !important;
        border-radius:10px !important;
        padding:10px 20px !important;
        font-size:16px !important;
        font-weight:600 !important;
        text-decoration:none !important;
        width:280px !important;
        text-align:center !important;
        transition:0.3s;
    }

    div.stLinkButton > a:hover{
        background:#5B5EF7 !important;
        transform:translateY(-2px);
        box-shadow:0px 5px 12px rgba(37,99,235,0.35);
    }

    </style>
    """, unsafe_allow_html=True)

    # ---------------- HEADER ----------------
    # st.markdown('<div class="title">Interview Hub</div>', unsafe_allow_html=True)
    st.markdown("""
                <h1 style="
                    font-size: 42px;
                    font-weight: 750;
                    color: #121F39;
                    margin-bottom: 5px;
                ">
                    Interview <span style="color:#5B5EF7;">Hub</span>
                </h1>
                """, unsafe_allow_html=True)
    st.markdown(
        '<div class="subtitle">Watch the best YouTube resources to prepare for placements and interviews.</div>',
        unsafe_allow_html=True
    )

    # ---------------- LINKS ----------------
    st.link_button(
        "Python Interview Questions",
        "https://www.youtube.com/results?search_query=python+interview+questions"
    )

    st.link_button(
        "Java Interview Questions",
        "https://www.youtube.com/results?search_query=java+interview+questions"
    )

    st.link_button(
        "DSA Interview Preparation",
        "https://www.youtube.com/results?search_query=dsa+interview+preparation"
    )

    st.link_button(
        "Aptitude Preparation",
        "https://www.youtube.com/results?search_query=aptitude+preparation+placements"
    )

    st.link_button(
        "HR Interview Tips",
        "https://www.youtube.com/results?search_query=hr+interview+questions"
    )

    st.link_button(
        "Resume Building Tips",
        "https://www.youtube.com/results?search_query=resume+building+for+freshers"
    )

    st.link_button(
        "Mock Interview Practice",
        "https://www.youtube.com/results?search_query=mock+interview+for+freshers"
    )