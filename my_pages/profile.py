def show_profile():
    import streamlit as st
    from components.header import render_header

    render_header()
    st.write("This is the **User Profile Page**.")