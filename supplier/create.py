# create.py

def show():
    import streamlit as st
    from utils.connection import get_supplier_collection
    from components.header import render_header
    from components.footer import render_footer
    from datetime import datetime

    render_header()

    collection = get_supplier_collection()

    st.title("Create Supplier")

    with st.form("create",clear_on_submit=True,  enter_to_submit=True, ):

        name = st.text_input("Name",value="")
        email = st.text_input("Email",value="")
        address = st.text_area("Address",value="")

        col=st.columns(3,gap="small")

        if col[0].form_submit_button("Add Supplier" , type="primary",use_container_width=True):
            if name :
                collection.insert_one({
                    "name": name,
                    "email":email,
                    "address":address,
                    "created_at": datetime.now()
                })
                st.success(f"Supplier {name} added successfully!")
                st.rerun()
            else:
                st.warning("Please fill both fields.")
        if col[1].form_submit_button("Show Supplier",type="primary",use_container_width=True):
            st.session_state.page="show_supplier"
            st.rerun()

    render_footer()