def show_system_logs():
    import streamlit as st
    from components.header import render_header

    render_header()
    st.write("This is the **System Logs Page**.")