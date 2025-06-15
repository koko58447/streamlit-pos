def show_preferences():
    import streamlit as st
    from components.header import render_header

    render_header()
    st.write("This is the **Preferences Page**.")