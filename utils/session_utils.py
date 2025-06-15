def initialize_session_state():
    import streamlit as st

    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
    if "theme" not in st.session_state:
        st.session_state.theme = "light"
    if "role" not in st.session_state:
        st.session_state.role = None  # 'user', 'admin'
    # Initialize session_state variables
    if "page" not in st.session_state:
        st.session_state.page = "home"
    if "language" not in st.session_state:
        st.session_state.language = "en"  # Default language: English