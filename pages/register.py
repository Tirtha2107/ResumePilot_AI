
import streamlit as st
import re
from db_config import get_connection
import bcrypt

# st.set_page_config(page_title=" AI Resume Analyzer - Register", layout="centered")

# --- CSS STYLING ---
st.markdown(
    """
    <style>
    [data-testid="stSidebar"] { display: none; }
    .stApp { background-color: #ffffff; }

    div.stButton > button {
        background-color: #5B5EF7;
        color: white;
        border-radius: 10px;
        padding: 10px 120px;
        font-size: 40px;
        font-style: bold;
        border: none;
        font-weight: 800;
        width: 100%;
    }
    div.stButton > button:hover {
        background-color: #5B5EF7;
        cursor: pointer;
    }

    .stTextInput input,
    .stTextArea textarea {
        background-color: #f2f2f2;
        color: #000000;
    }

    [data-testid="stWidgetLabel"] p,
    [data-testid="stWidgetLabel"] div {
        color: #000000 !important;
    }

    .stTextInput input::placeholder,
    .stTextArea textarea::placeholder {
        color: #555555;
        opacity: 1;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# --- TITLES ---
# st.markdown(
#     "<h1 style='text-align:center; color:#111827; font-family:Arial, sans-serif;'>AI Resume Analyzer</h1>",
#     unsafe_allow_html=True,
# )

st.markdown("""
            <h1 style="
                font-size: 42px;
                font-weight: 750;
                color: #121F39;
                text-align: center;
                margin-bottom: 5px;
            ">
                ResumePilot <span style="color:#5B5EF7;">AI</span>
            </h1>
""", unsafe_allow_html=True)
st.markdown(
    "<h3 style='text-align:center; font-family:Arial, sans-serif; color:#111827;'>Register</h3>",
    unsafe_allow_html=True,
)
st.write("")

# --- VALIDATION FUNCTIONS ---
def validate_name(value: str) -> bool:
    return re.match(r"^[A-Za-z ]{2,}$", value) is not None

def validate_email_strict(email: str) -> str:
    email = email.strip()
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    if not re.match(pattern, email):
        return "Invalid email format."
    domain = email.split('@')[1].lower()
    if domain in ["gmail.co", "yahoo.co", "hotmail.co"]:
        return f"Invalid domain '{domain}'. Did you mean .com?"
    return None

def validate_indian_phone(value: str) -> bool:
    return re.match(r"^[6-9]\d{9}$", value) is not None

st.markdown("<h4 style='color:#111827;'>Basic Details</h4>", unsafe_allow_html=True)

full_name = st.text_input(
    "Full Name",
    placeholder="Enter your full name"
)

email = st.text_input(
    "Email",
    placeholder="Enter your email"
)

password = st.text_input(
    "Password",
    type="password"
)

confirm_password = st.text_input(
    "Confirm Password",
    type="password"
)

age = st.number_input(
    "Age",
    min_value=15,
    max_value=80,
    step=1
)

# # --- FORM ---
# st.markdown("<h4 style='color:#000000;'>Basic Details</h4>", unsafe_allow_html=True)
st.markdown("<h4 style='color:#111827;'>Educational Details</h4>", unsafe_allow_html=True)

qualification = st.selectbox(
    "Highest Qualification",
    [
        "Select",
        "SSC",
        "HSC",
        "Diploma",
        "B.E.",
        "B.Tech",
        "M.E.",
        "M.Tech",
        "BCA",
        "MCA",
        "B.Sc",
        "M.Sc",
        "Other"
    ]
)

branch = st.text_input(
    "Branch / Specialization",
    placeholder="e.g. Computer Engineering"
)

college = st.text_input(
    "College / University",
    placeholder="Enter your college name"
)

passing_year = st.text_input(
    "Passing Year",
    placeholder="e.g. 2026"
)

contact = st.text_input(
    "Contact Number",
    placeholder="Enter your 10-digit mobile number"
)



col1, col2 = st.columns(2)

with col1:
    if st.button("Register"):

        if not full_name.strip():
            st.error("Please enter your full name.")

        elif not validate_name(full_name):
            st.error("Name should contain only letters and spaces.")

        elif not email.strip():
            st.error("Please enter your email.")

        else:
            email_error = validate_email_strict(email)

            if email_error:
                st.error(email_error)

            elif len(password) < 6:
                st.error("Password must contain at least 6 characters.")

            elif password != confirm_password:
                st.error("Passwords do not match.")

            elif qualification == "Select":
                st.error("Please select your qualification.")

            elif not branch.strip():
                st.error("Please enter your branch.")

            elif not college.strip():
                st.error("Please enter your college name.")

            elif not passing_year.isdigit():
                st.error("Please enter a valid passing year.")

            elif not validate_indian_phone(contact):
                st.error("Please enter a valid 10-digit mobile number.")

            else:
                conn = get_connection()
                cursor = conn.cursor()

                try:
                    # Check if email already exists
                    cursor.execute(
                        "SELECT * FROM users WHERE email=?",
                        (email,)
                    )

                    if cursor.fetchone():
                        st.error("Email already registered.")

                    else:
                        # Hash the password
                        hashed_password = bcrypt.hashpw(
                            password.encode("utf-8"),
                            bcrypt.gensalt()
                        ).decode("utf-8")
                        cursor.execute("""
                        INSERT INTO users
                        (full_name, email, password, age, qualification, branch, college, passing_year, contact)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                        """,
                        (
                            full_name,
                            email,
                            hashed_password,
                            age,
                            qualification,
                            branch,
                            college,
                            int(passing_year),
                            contact
                        ))

                        conn.commit()
                        st.success("Registration Successful! Redirecting to Login...")

                        import time
                        time.sleep(2)

                        st.switch_page("pages/login.py")

                except Exception as e:
                    st.error(f"Error: {e}")

                finally:
                    conn.close()

with col2:
    if st.button("Go to Login"):
        st.switch_page("pages/login.py")
