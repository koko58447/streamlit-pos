def show():
    import streamlit as st
    from utils.connection import get_remains_with_details
    import pandas as pd
    import base64
    from components.header import render_header
    from components.footer import render_footer

    render_header()

    st.title("Inventory List")

    # Get data from MongoDB using aggregation
    items = get_remains_with_details()
    
    if not items:
        st.info("No inventory found.")
        return

    # Convert to DataFrame
    df = pd.DataFrame(items)

    # Show all columns in DataFrame for debugging
    # st.write(df.columns.tolist())  # Uncomment this line if you want to check available columns

    # Search functionality
    search_term = st.text_input("Search by Code ,Item Name, Category or Supplier")
    if search_term:
        df = df[df.apply(lambda row: 
            any(
                search_term.lower() in str(val).lower() 
                for val in [row['code'],row['item_name'], row['category_name'], row['supplier_name']]
            ), axis=1)]

    # Define display columns only (remove unwanted ones)
    display_columns = ['Select','code', 'item_name', 'category_name', 'supplier_name', 'remain_stock', 'remain_price', 'create_at']

    # Add Select column
    df['Select'] = False
    display_df = df[display_columns]

    # Rename columns for UI display
    custom_column_names = {
        'code':'Code',
        'item_name': 'Item Name',
        'category_name': 'Category',
        'supplier_name': 'Supplier',
        'remain_stock': 'Stock Qty',
        'remain_price': 'Price',
        'create_at': 'Created At'
    }
    display_df.rename(columns=custom_column_names, inplace=True)

    # Show data editor
    edited_df = st.data_editor(display_df, hide_index=True, use_container_width=True, key='data_editor')

    # Action Buttons
    col = st.columns(4, gap="small")

    with col[0].popover("Export:", use_container_width=True):
        st.markdown("### Export Data")
        filtered_data = df.drop(columns=['Select'], errors='ignore')

        # CSV Download
        if st.button("Export as CSV", key="export_csv", use_container_width=True):
            csv = filtered_data.to_csv(index=False).encode('utf-8')
            b64 = base64.b64encode(csv).decode()
            href = f'<a download="inventory.csv" href="data:text/csv;base64,{b64}" target="_blank">Download CSV</a>'
            st.markdown(href, unsafe_allow_html=True)

        # Excel Download
        if st.button("Export as Excel", key="export_excel", use_container_width=True):
            from io import BytesIO
            output = BytesIO()
            with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                filtered_data.to_excel(writer, sheet_name='Inventory', index=False)
            excel_data = output.getvalue()
            b64 = base64.b64encode(excel_data).decode()
            mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            href = f'<a download="inventory.xlsx" href="data:{mime_type};base64,{b64}" target="_blank">Download Excel</a>'
            st.markdown(href, unsafe_allow_html=True)

    render_footer()