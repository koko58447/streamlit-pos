def show_update():
    import streamlit as st
    from utils.connection import get_user_collection
    from bson.objectid import ObjectId

    collection = get_user_collection()

    st.title("Update User")

    if "edit_user" in st.session_state:
        user = st.session_state.edit_user
        user_id = user["_id"]

        with st.container(border=True,):
            name = st.text_input("Name", value=user["name"])
            email = st.text_input("Email", value=user["email"])

            # Columns with zero gap
            col = st.columns(4,gap="small")
            
          
            update_button = col[0].button("Update",type="primary",use_container_width=True)
            back_button = col[1].button("Back", type="primary",use_container_width=True)

            if update_button:
                collection.update_one(
                    {"_id": ObjectId(user_id)},
                    {"$set": {"name": name, "email": email}}
                )
                st.success("User updated successfully!")
                del st.session_state.edit_user
                st.session_state.page = "show"
                st.rerun()

            if back_button:
                st.session_state.page = "show"
                st.rerun()

    else:
        st.warning("No user selected for editing.")
        if st.button("Go back"):
            st.session_state.page = "show"
            st.rerun()