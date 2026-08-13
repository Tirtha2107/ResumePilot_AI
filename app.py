import streamlit as st
from streamlit_option_menu import option_menu
from pages.upload_resume import resume
from pages.profile import profile
from pages.job_matcher import job_matcher
from pages.interview import interview
from pages.hub import hub
from pages.AI_ass import AI
from pages.roadmap import map


st.set_page_config(
    page_title="AI Resume Analyzer",
    layout="wide"
)

# Login check
if "logged_in" not in st.session_state or not st.session_state["logged_in"]:
    st.switch_page("pages/login.py")

# ---------------- PAGE ----------------
st.set_page_config(
    page_title="ResumePilot AI",
    layout="wide"
)

# st.title("AI Resume Analyzer & Job Recommendation System")

st.markdown("""
<style>

/* Hide app/login/register list */
[data-testid="stSidebarNav"]{
    display:none;
}

</style>

""", unsafe_allow_html=True)
st.markdown("""
    <style>

    /* ---------- Buttons ---------- */

    div.stButton > button{
        background:#5B5EF7;
        color:white;
        border:none;
        border-radius:12px;
        height:55px;
        font-size:36px;
        font-weight:600;
        transition:0.3s;
    }

    div.stButton > button:hover{
        background:#5B5EF7;
        color:white;
        transform:translateY(-2px);
        box-shadow:0px 8px 20px rgba(37,99,235,0.35);
    }

    /* ---------- Blue Container ---------- */

    .blue-box{

        background: #121F39;
        padding: 30px 100px;

        border-radius: 18px;

        color: white;

        width: 100%;
        margin-top: -59px;
        margin-bottom: 25px;

        box-shadow: 0px 8px 20px rgba(37,99,235,0.25);
        box-sizing: border-box;

    }

    .blue-title{

        font-size:40px;

        font-weight:bold;

    }

    .blue-text{

        font-size:16px;

        opacity:0.95;

    }


    </style>
    """,unsafe_allow_html=True)

st.markdown("""
        <div class="blue-box">

        <div class="blue-title">
        ResumePilot AI
        </div>

        <div class="blue-text">

        AI-Powered Resume Analysis, Job Matching & Interview Preparation

        </div>

        </div>
        """,unsafe_allow_html=True)


st.markdown("""
<style>

/* Sidebar background */
[data-testid="stSidebar"] {
    background-color: #121F39;
}

/* Sidebar spacing */
[data-testid="stSidebar"] > div:first-child {
    padding-top: 20px;
}


/* =========================
   BRAND
   ========================= */

.sidebar-brand {
    text-align: center;
    color: white;
    font-size: 22px;
    font-weight: 800;
    line-height: 1.2;
    margin-bottom: 18px;
}

.sidebar-brand span {
    color: #5B5EF7;
}


/* =========================
   PROFILE
   ========================= */

.profile-name {
    color: white;
    font-size: 15px;
    font-weight: 700;
}

.profile-welcome {
    color: #C8D0E8;
    font-size: 12px;
}


/* =========================
   NAVIGATION TITLE
   ========================= */

.nav-title {
    color: #9CA8C7;
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 2px;
    margin-top: 15px;
    margin-bottom: 8px;
}

</style>
""", unsafe_allow_html=True)


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    # -----------------------------------------------------
    # AI RESUME ANALYZER
    # -----------------------------------------------------

    st.markdown(
        """
        <h2 style="
            color:white;
            text-align:center;
            font-size:32px;
            font-weight:800;
            line-height:1.2;
            margin-bottom:18px;
        ">
            ResumePilot<br>
            <span style="color:#5B5EF7;">AI ✦</span>
        </h2>
        """,
        unsafe_allow_html=True
    )


    # -----------------------------------------------------
    # PROFILE
    # -----------------------------------------------------

    user_name = st.session_state.get("first_name", "User")

    st.markdown(
        f"""
        <p style="
            color:white;
            font-size:15px;
            font-weight:700;
            margin-bottom:2px;
        ">
            &nbsp; {st.session_state['user_name']}
        </p>

        <p style="
            color:#C8D0E8;
            font-size:12px;
            margin-top:0px;
            margin-bottom:18px;
        ">
            Welcome Back! 
        </p>
        """,
        unsafe_allow_html=True
    )


    # -----------------------------------------------------
    # NAVIGATION TITLE
    # -----------------------------------------------------

    st.markdown(
        """
        <p style="
            color:#9CA8C7;
            font-size:11px;
            font-weight:700;
            letter-spacing:2px;
            margin-bottom:8px;
        ">
            NAVIGATION
        </p>
        """,
        unsafe_allow_html=True
    )


    # -----------------------------------------------------
    # MENU
    # -----------------------------------------------------

    selected = option_menu(
        menu_title=None,

        options=[
            "Resume Analyzer",
            "Job Matcher",
            "Interview Roadmap",
            "Interview Guide",
            "AI Assistant",
            "Interview Hub",
            "Profile",
            "Logout"
        ],

        icons=[
            "cloud-upload-fill",
            "briefcase-fill",
            "signpost-split-fill",
            "journal-text",
            "robot",
            "play-fill",
            "person-circle",
            "box-arrow-right"
        ],

        default_index=0,

        styles={
            "container": {
                "padding": "0px",
                "background-color": "#121F39",
            },

            "icon": {
                "color": "#5B5EF7",
                "font-size": "17px",
            },

            "nav-link": {
                "font-size": "15px",
                "text-align": "left",
                "margin": "3px 0px",
                "padding": "9px 12px",
                "--hover-color": "#121F39",
                "color": "white",
                "border-radius": "9px",
            },

            "nav-link-selected": {
                "background-color": "#5B5EF7",
                "color": "white",
            },
        }
    )

if selected == "Resume Analyzer":
    resume()
    
elif selected == "Job Matcher":
    job_matcher()
elif selected == "Interview Roadmap":
    map()

elif selected == "Interview Guide":
    interview()

elif selected == "AI Assistant":
    AI()


elif selected == "Interview Hub":
    hub()

elif selected == "Profile":
    import streamlit as st
    
    # ---------------- PAGE CONFIG ----------------
    st.set_page_config(
        page_title="AI Resume Analyzer",
        layout="wide"
    )
    st.write("User Profile")
    profile()

elif selected == "Logout":
    st.session_state.clear()
    st.switch_page("pages/login.py")

