def show_home():
    import streamlit as st
    from components.header import render_header
    from components.footer import render_footer

    render_header()
    st.write("This is the Home Page.")
    render_footer()