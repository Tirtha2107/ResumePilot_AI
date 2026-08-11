def profile():
    import streamlit as st
    from db_config import get_connection

   

    st.set_page_config(
        page_title="My Profile",
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
        padding: 20px;
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
        font-size: 15px;
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



    st.title("My Profile")


    

    with st.container(border=True):

     

        initial = full_name[0].upper() if full_name else "U"

        st.markdown(
            f"""
            <div style="
                width:80px;
                height:80px;
                border-radius:50%;
                background:#5B5EF7;
                color:white;
                display:flex;
                align-items:center;
                justify-content:center;
                margin:0 auto 15px auto;
                font-size:32px;
                font-weight:bold;
            ">
                {initial}
            </div>
            """,
            unsafe_allow_html=True
        )


  

        st.markdown(
            f"""
            <h2 style="
                text-align:center;
                color:#5B5EF7;
                margin-bottom:5px;
            ">
                {full_name}
            </h2>
            """,
            unsafe_allow_html=True
        )



        st.markdown(
            f"""
            <p style="
                text-align:center;
                color:gray;
                margin-bottom:20px;
            ">
                {email}
            </p>
            """,
            unsafe_allow_html=True
        )


        st.divider()


        

        c1, c2 = st.columns(2)


        with c1:

            st.markdown("**Age**")
            st.write(age if age else "Not provided")

            st.markdown("**Qualification**")
            st.write(qualification if qualification else "Not provided")

            st.markdown("**Branch**")
            st.write(branch if branch else "Not provided")

            st.markdown("**Contact Number**")
            st.write(contact if contact else "Not provided")


        

        with c2:

            st.markdown("**College**")
            st.write(college if college else "Not provided")

            st.markdown("**Passing Year**")
            st.write(passing_year if passing_year else "Not provided")

            st.markdown("**Email**")
            st.write(email)


        st.divider()


        

        b1, b2 = st.columns(2)



        with b1:

            if st.button(
                "Edit Profile",
                use_container_width=True
            ):

                st.switch_page("pages/edit_profile.py")


       

        with b2:

            if st.button(
                "Logout",
                use_container_width=True
            ):

                st.session_state.clear()
                st.switch_page("pages/login.py")

