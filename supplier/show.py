def show():
    import streamlit as st
    from utils.connection import get_supplier_collection
    from bson.objectid import ObjectId
    import pandas as pd
    import base64

    collection = get_supplier_collection()

    st.title("Supplier List")

    # Fetch users from MongoDB
    users = list(collection.find())
    
    if not users:
        st.info("No Supplier found.")
        # return

    # Convert to DataFrame
    df = pd.DataFrame(users)

    search_term = st.text_input("Search by Name or Email or address")

    # Apply filter
    if search_term:
        df = df[df.apply(lambda row: 
            (search_term.lower() in str(row['name']).lower()) or 
            (search_term.lower() in str(row['email']).lower()) or 
            (search_term.lower() in str(row['address']).lower()), 
        axis=1)]
    # Remove _id column for display
    display_df = df.drop(columns=['_id'], errors='ignore')

    # Add Select column
    display_df['Select'] = False
    cols = ['Select'] + [col for col in display_df.columns if col != 'Select']
    display_df = display_df[cols]

    # Show data editor (without _id)
    edited_df = st.data_editor(display_df, hide_index=True, use_container_width=True, key='data_editor')
    # Action buttons
    col = st.columns(4,gap="small")
    if col[0].button("New",type="primary",use_container_width=True):
         st.session_state.page="create_supplier"
         st.rerun()
    if col[1].button("Edit", type="primary",use_container_width=True):
            selected_rows = edited_df[edited_df['Select']]
            
            if len(selected_rows) == 0:
                st.warning("Please select a supplier to edit.")
            elif len(selected_rows) > 1:
                st.warning("Please select only one supplier.")
            else:
                original_selected = df[df.index.isin(selected_rows.index)]
                selected_user = original_selected.iloc[0].to_dict()
                
                # Store selected user in session state
                st.session_state.edit_category = {
                    '_id': selected_user['_id'],
                    'name': selected_user['name'],
                    'email': selected_user['email'],
                    'address': selected_user['address'],
                }
                st.session_state.page = "update_supplier"
                st.rerun()
  
    if col[2].button("Delete", type="primary",use_container_width=True):
            selected_rows = edited_df[edited_df['Select']]
            
            if len(selected_rows) == 0:
                st.warning("Please select at least one supplier to delete.")
            else:
                original_selected = df[df.index.isin(selected_rows.index)]
                for _, row in original_selected.iterrows():
                    collection.delete_one({"_id": ObjectId(row["_id"])})
                st.success(f"{len(selected_rows)} supplier(s) deleted successfully!")
                st.rerun()

 

        # Export Popover
    with col[3].popover("Export:",use_container_width=True):
        st.markdown("### Export Data")

        filtered_data = df.drop(columns=['Select'], errors='ignore')
        
        # CSV Download
        if st.button("Export as CSV", key="export_csv",use_container_width=True):
            csv = filtered_data.to_csv(index=False).encode('utf-8')
            b64 = base64.b64encode(csv).decode()
            href = f'<a download="supplier.csv" href="data:text/csv;base64,{b64}" target="_blank">Click here to download CSV</a>'
            st.markdown(href, unsafe_allow_html=True)

        # Excel Download
        if st.button("Export as Excel", key="export_excel",use_container_width=True):
            from io import BytesIO
            output = BytesIO()
            with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                filtered_data.to_excel(writer, sheet_name='Users', index=False)
            excel_data = output.getvalue()
            b64 = base64.b64encode(excel_data).decode()
            mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            href = f'<a download="supplier.xlsx" href="data:{mime_type};base64,{b64}" target="_blank">Click here to download Excel</a>'
            st.markdown(href, unsafe_allow_html=True)