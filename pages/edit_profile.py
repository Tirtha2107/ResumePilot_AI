import streamlit as st
from db_config import get_connection


st.set_page_config(
    page_title="Edit Profile",
    layout="wide"
)

st.markdown("""
<style>

.stApp {
    background: #F5F7FB;
}

div[data-testid="stVerticalBlockBorderWrapper"] {
    border: 1px solid #E5E7EB;
    border-radius: 18px;
    padding: 25px;
    background: white;
    box-shadow: 0px 4px 12px rgba(0,0,0,0.08);
}

.stButton > button {
    width: 100%;
    background: #5B5EF7;
    color: white;
    border: none;
    border-radius: 10px;
    height: 45px;
    font-weight: 600;
}

.stButton > button:hover {
    background: #4B4EE5;
    color: white;
}

</style>
""", unsafe_allow_html=True)


if "user_email" not in st.session_state:

    st.error("Please login first.")
    st.stop()


email = st.session_state["user_email"]

conn = get_connection()
cursor = conn.cursor()

cursor.execute("""
    SELECT
        full_name,
        email,
        age,
        qualification,
        branch,
        college,
        passing_year,
        contact
    FROM users
    WHERE email = ?
""", (email,))

user = cursor.fetchone()

conn.close()


if user is None:

    st.error("User not found.")
    st.stop()


full_name, email, age, qualification, branch, college, passing_year, contact = user


st.title("Edit Profile")

st.caption("Update your personal and academic information.")



with st.container(border=True):

    c1, c2 = st.columns(2)

    with c1:

        new_name = st.text_input(
            "Full Name",
            value=full_name or ""
        )

        new_age = st.number_input(
            "Age",
            min_value=1,
            max_value=100,
            value=int(age) if age else 18
        )

        new_qualification = st.text_input(
            "Qualification",
            value=qualification or ""
        )

        new_branch = st.text_input(
            "Branch",
            value=branch or ""
        )


    with c2:

        new_college = st.text_input(
            "College",
            value=college or ""
        )

        new_passing_year = st.number_input(
            "Passing Year",
            min_value=2000,
            max_value=2100,
            value=int(passing_year) if passing_year else 2026
        )

        new_contact = st.text_input(
            "Contact Number",
            value=contact or ""
        )

        st.text_input(
            "Email",
            value=email,
            disabled=True
        )


    st.divider()


    save_col, cancel_col = st.columns(2)


    with save_col:

        if st.button(
            "Save Changes",
            use_container_width=True
        ):

            # ---------------- VALIDATION ----------------

            if not new_name.strip():
                st.error("Please enter your full name.")
                st.stop()

            if not new_qualification.strip():
                st.error("Please enter your qualification.")
                st.stop()

            if not new_branch.strip():
                st.error("Please enter your branch.")
                st.stop()

            if not new_college.strip():
                st.error("Please enter your college.")
                st.stop()

            if not new_contact.strip():
                st.error("Please enter your contact number.")
                st.stop()

            if not new_contact.isdigit():
                st.error("Contact number should contain only digits.")
                st.stop()

            if len(new_contact) != 10:
                st.error("Contact number must contain exactly 10 digits.")
                st.stop()

            conn = get_connection()
            cursor = conn.cursor()

            cursor.execute("""
                UPDATE users
                SET
                    full_name = ?,
                    age = ?,
                    qualification = ?,
                    branch = ?,
                    college = ?,
                    passing_year = ?,
                    contact = ?
                WHERE email = ?
            """, (
                new_name.strip(),
                new_age,
                new_qualification.strip(),
                new_branch.strip(),
                new_college.strip(),
                new_passing_year,
                new_contact.strip(),
                email
            ))

            if cursor.rowcount == 0:

                conn.close()

                st.error(
                    "Profile could not be updated. "
                    "User email was not found in the database."
                )

                st.stop()

            conn.commit()
            conn.close()



            st.success("Profile updated successfully!")

            # Go back to profile page
            st.switch_page("pages/profile.py")


    with cancel_col:

        if st.button(
            "Cancel",
            use_container_width=True
        ):

            st.switch_page("pages/profile.py")

