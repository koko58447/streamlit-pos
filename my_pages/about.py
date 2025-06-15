def show_about():
    import streamlit as st
    from components.header import render_header
    from components.footer import render_footer

    render_header()
    st.write("This is the About Page.")
    render_footer()