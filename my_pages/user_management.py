def show_user_management():
    import streamlit as st
    from components.header import render_header

    render_header()
    st.write("This is the **User Management Page**.")