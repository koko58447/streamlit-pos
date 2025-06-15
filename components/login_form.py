def render_login_form():
    import streamlit as st

    st.title("🔐 Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username == "admin" and password == "1":
            st.session_state.logged_in = True
            st.session_state.role = "admin"
            st.success("Logged in as Admin!")
            st.rerun()
        elif username == "user" and password == "1":
            st.session_state.logged_in = True
            st.session_state.role = "user"
            st.success("Logged in as User!")
            st.rerun()
        else:
            st.error("Invalid credentials")