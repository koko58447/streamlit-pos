def show():
    import streamlit as st
    from utils.connection import get_supplier_collection
    from bson.objectid import ObjectId
    from datetime import datetime

    collection = get_supplier_collection()

    st.title("Update Supplier")

    if "edit_category" in st.session_state:
        user = st.session_state.edit_category
        user_id = user["_id"]

        with st.container(border=True,):
            name = st.text_input("Name", value=user["name"])
            email = st.text_input("Email", value=user["email"])
            address = st.text_area("Address", value=user["address"])
            # Columns with zero gap
            col = st.columns(4,gap="small")
            
          
            update_button = col[0].button("Update",type="primary",use_container_width=True)
            back_button = col[1].button("Back", type="primary",use_container_width=True)

            if update_button:
                collection.update_one(
                    {"_id": ObjectId(user_id)},
                    {"$set": {
                        "name": name,
                        "email":email,
                        "address":address,                         
                          "created_at": datetime.now()}}
                )
                st.success("Supplier updated successfully!")
                del st.session_state.edit_category
                st.session_state.page = "show_supplier"
                st.rerun()

            if back_button:
                st.session_state.page = "show_supplier"
                st.rerun()

    else:
        st.warning("No Supplier selected for editing.")
        if st.button("Go back"):
            st.session_state.page = "show_supplier"
            st.rerun()