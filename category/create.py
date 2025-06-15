# create.py

def show_create():
    import streamlit as st
    from utils.connection import get_category_collection
    from components.header import render_header
    from components.footer import render_footer
    from datetime import datetime

    render_header()

    collection = get_category_collection()

    st.title("Create Category")

    with st.form("create",clear_on_submit=True,  enter_to_submit=True, ):

        name = st.text_input("Name",value="")

        col=st.columns(3,gap="small")

        if col[0].form_submit_button("Add User" , type="primary",use_container_width=True):
            if name :
                collection.insert_one({
                    "name": name,
                    "created_at": datetime.now()
                })
                st.success(f"Category {name} added successfully!")
                st.rerun()
            else:
                st.warning("Please fill both fields.")
        if col[1].form_submit_button("Show User",type="primary",use_container_width=True):
            st.session_state.page="show_category"
            st.rerun()

    render_footer()