def show():
    import streamlit as st
    from utils.connection import get_item_collection, get_category_collection, get_supplier_collection
    from bson.objectid import ObjectId

    item_collection = get_item_collection()
    category_collection = get_category_collection()
    supplier_collection = get_supplier_collection()

    st.title("Update Item")

    if "edit_item" in st.session_state:
        item = st.session_state.edit_item
        item_id = item["_id"]

        # Get all categories and suppliers for dropdown
        categories = list(category_collection.find({}, {"name": 1}))
        suppliers = list(supplier_collection.find({}, {"name": 1}))

        # Convert to name -> id mapping
        category_options = {str(cat["_id"]): cat["name"] for cat in categories}
        supplier_options = {str(supp["_id"]): supp["name"] for supp in suppliers}

        with st.container(border=True):
            st.subheader("Edit Item")
            code = st.text_input("Code", value=item.get("code", ""))
            name = st.text_input("Name", value=item.get("name", ""))
            price = st.number_input("Price", min_value=0.0, value=float(item.get("price", 0)), step=0.1)
            stock = st.number_input("Qty", min_value=0, value=int(item.get("qty", 0)), step=1)

            # Category Dropdown
            selected_category_id = item.get("category_id", None)
            category_id = st.selectbox(
                "Category",
                options=list(category_options.keys()),
                format_func=lambda x: category_options[x],
                index=list(category_options.keys()).index(str(selected_category_id)) if selected_category_id else 0
            )

            # Supplier Dropdown
            selected_supplier_id = item.get("supplier_id", None)
            supplier_id = st.selectbox(
                "Supplier",
                options=list(supplier_options.keys()),
                format_func=lambda x: supplier_options[x],
                index=list(supplier_options.keys()).index(str(selected_supplier_id)) if selected_supplier_id else 0
            )

            col = st.columns(4, gap="small")
            update_button = col[0].button("Update", type="primary", use_container_width=True)
            back_button = col[1].button("Back", use_container_width=True)

            if update_button:
                item_collection.update_one(
                    {"_id": ObjectId(item_id)},
                    {
                        "$set": {
                            "code":code,
                            "name": name,
                            "price": price,
                            "qty": stock,
                            "category_id": ObjectId(category_id),
                            "supplier_id": ObjectId(supplier_id)
                        }
                    }
                )
                st.success("Item updated successfully!")
                del st.session_state.edit_item
                st.session_state.page = "show_item"
                st.rerun()

            if back_button:
                st.session_state.page = "show_item"
                st.rerun()

    else:
        st.warning("No item selected for editing.")
        if st.button("Go Back"):
            st.session_state.page = "show_item"
            st.rerun()