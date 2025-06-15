def show():
    import streamlit as st
    from utils.connection import get_category_collection
    from bson.objectid import ObjectId
    from datetime import datetime

    collection = get_category_collection()

    st.title("Update User")

    if "edit_category" in st.session_state:
        user = st.session_state.edit_category
        user_id = user["_id"]

        with st.container(border=True,):
            name = st.text_input("Name", value=user["name"])
           
            # Columns with zero gap
            col = st.columns(4,gap="small")
            
          
            update_button = col[0].button("Update",type="primary",use_container_width=True)
            back_button = col[1].button("Back", type="primary",use_container_width=True)

            if update_button:
                collection.update_one(
                    {"_id": ObjectId(user_id)},
                    {"$set": {"name": name, "created_at": datetime.now()}}
                )
                st.success("Category updated successfully!")
                del st.session_state.edit_category
                st.session_state.page = "show_category"
                st.rerun()

            if back_button:
                st.session_state.page = "show_category"
                st.rerun()

    else:
        st.warning("No Category selected for editing.")
        if st.button("Go back"):
            st.session_state.page = "show"
            st.rerun()