from pages import technical_round


def interview():
    import streamlit as st
    from pages import aptitude
    from pages import technical_round
    from pages import mock
    st.set_page_config(page_title="Interview Guide", layout="wide")
   

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

    </style>
    """,unsafe_allow_html=True)

    st.markdown("""
                    <h1 style="
                        font-size: 42px;
                        font-weight: 750;
                        color: #121F39;
                        margin-bottom: 5px;
                    ">
                        Interview <span style="color:#5B5EF7;">Preparation Guide</span>
                    </h1>
    """, unsafe_allow_html=True)
   

    

    st.write("")

    col1,col2,col3=st.columns(3)

    with col1:
        if st.button("Aptitude Practice",use_container_width=True):
            st.session_state.page="aptitude"

    with col2:
        if st.button("Technical Round",use_container_width=True):
            st.session_state.page="technical"

    with col3:
        if st.button("AI HR Interview",use_container_width=True):
            st.session_state.page="mock"




    st.divider()

    page=st.session_state.get("page","roadmap")
