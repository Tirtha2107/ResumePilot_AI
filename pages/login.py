import streamlit as st
import re
import bcrypt
from db_config import get_connection



# ---------- CSS ----------
st.markdown("""
<style>
[data-testid="stSidebar"]{
    display:none;
}

.stApp{
    background-color:white;
}

div.stButton > button{
    background:#5B5EF7;
    color:white;
    border-radius:10px;
    border:none;
    width:100%;
    font-weight:600;
    padding:8px;
}

div.stButton > button:hover{
    background:#4B4EF0;
}

.stTextInput input{
    background:#f2f2f2;
    color:black;
}

[data-testid="stWidgetLabel"] p{
    color:black;
}
</style>
""", unsafe_allow_html=True)



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
    "<h3 style='text-align:center;'>User Login</h3>",
    unsafe_allow_html=True
)


# ---------- VALIDATION ----------
def validate_email(email):
    pattern = r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$'
    return re.match(pattern, email)


def validate_phone(phone):
    return re.match(r'^[6-9]\d{9}$', phone)


# ---------- INPUT ----------
username = st.text_input(
    "Email or Phone Number",
    placeholder="Enter email or mobile number"
)

password = st.text_input(
    "Password",
    type="password"
)

col1, col2 = st.columns(2)

# ---------- LOGIN ----------
with col1:

    if st.button("Login"):

        if username.strip() == "":
            st.error("Please enter Email or Phone Number.")

        elif password.strip() == "":
            st.error("Please enter Password.")

        else:

            conn = get_connection()
            cursor = conn.cursor()

            # Login using Email
            if "@" in username:

                if not validate_email(username):
                    st.error("Invalid Email Format.")
                    conn.close()
                    st.stop()

                cursor.execute(
                    "SELECT * FROM users WHERE email=?",
                    (username,)
                )

            # Login using Phone
            else:

                if not validate_phone(username):
                    st.error("Invalid Mobile Number.")
                    conn.close()
                    st.stop()

                cursor.execute(
                    "SELECT * FROM users WHERE contact=?",
                    (username,)
                )

            user = cursor.fetchone()
            conn.close()

            if user is None:
                st.error("Account not found.")
            else:

                stored_password = user[3]
                if bcrypt.checkpw(
                        password.encode("utf-8"),
                        stored_password.encode("utf-8")
                ):

                    # Create login session
                    st.session_state["logged_in"] = True
                    st.session_state["user_id"] = user[0]
                    st.session_state["user_name"] = user[1]
                    st.session_state["user_email"] = user[2]

                    st.success(f"Welcome {user[1]}!")

                    import time
                    time.sleep(1)

                    st.switch_page("app.py")

                else:
                    st.error("Invalid Email/Phone or Password.")
              


# ---------- REGISTER ----------
with col2:

    if st.button("New User? Register"):
        st.switch_page("pages/register.py")