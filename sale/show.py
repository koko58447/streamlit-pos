# def show():
#     import streamlit as st
#     from utils.connection import get_sales_collection
#     import pandas as pd

#     st.title("🧾 Sales History")

#     sales = list(get_sales_collection().find())

#     if not sales:
#         st.info("No sales records found.")
#         return

#     for sale in sales:
#         with st.expander(f"Receipt #{str(sale['_id'])} — {sale['customer_name']}"):
#             st.write(f"**Customer:** {sale['customer_name']}")
#             st.write(f"**Phone:** {sale['phone']}")
#             st.write(f"**Total Amount:** {sale['total_amount']}")
#             st.markdown("---")
#             df = pd.DataFrame(sale["items"])
#             st.dataframe(df[["code", "name", "qty", "price"]], hide_index=True, use_container_width=True)

import streamlit as st
from utils.connection import get_sales_collection
import pandas as pd
from datetime import datetime
import base64
from io import BytesIO
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch

def show():
    

    sales_collection = get_sales_collection()
    
    st.title("🧾 Sales History")

    # Filter Options
    col1, col2 = st.columns(2)
    with col1:
        customer_filter = st.text_input("Filter by Customer Name")
    with col2:
        date_filter = st.date_input("Filter by Date", value=None)

    # Fetch and filter data
    sales = list(sales_collection.find())
    filtered_sales = []

    for sale in sales:
        match = True
        if customer_filter and customer_filter.lower() not in sale.get("customer_name", "").lower():
            match = False
        if date_filter:
            sale_date = sale.get("created_at")
            if sale_date and sale_date.date() != date_filter:
                match = False
        if match:
            filtered_sales.append(sale)

    if not filtered_sales:
        st.info("No matching sales records found.")
        return

    # Export Buttons
    col_export1, col_export2 = st.columns(2)
    if col_export1.button("Export to Excel"):
        export_to_excel(filtered_sales)
    if col_export2.button("Export to PDF"):
        export_to_pdf(filtered_sales)

    # Display Sales
    for sale in filtered_sales:
        with st.expander(f"Receipt #{str(sale['_id'])} — {sale['customer_name']} — {sale['created_at'].strftime('%Y-%m-%d %H:%M')}"):
            st.markdown(f"**Customer:** {sale['customer_name']}")
            st.markdown(f"**Phone:** {sale['phone']}")
            st.markdown(f"**Total Amount:** `{sale['total_amount']}`")
            st.markdown(f"**Date:** {sale['created_at']}")

            items = sale.get("items", [])
            formatted_items = format_items(items)
            if formatted_items:
                df = pd.DataFrame(formatted_items)
                st.dataframe(df[["code", "name", "qty", "price"]], hide_index=True, use_container_width=True)
            else:
                st.warning("No items found in this receipt.")

# ────────────────────────
# Helper Functions
# ────────────────────────

def format_items(items):
    """Convert items to uniform dict format"""
    formatted = []
    for item in items:
        if isinstance(item, list):  # ['a001', 'item1', 2, 20.0]
            formatted.append({
                "code": item[0],
                "name": item[1],
                "qty": item[2],
                "price": item[3]
            })
        elif isinstance(item, dict):  # {"code": "...", ...}
            formatted.append({
                "code": item.get("code", ""),
                "name": item.get("name", ""),
                "qty": item.get("qty", 0),
                "price": item.get("price", 0.0)
            })
    return formatted

def export_to_excel(sales):
    """Export all sales to Excel file"""
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        for i, sale in enumerate(sales):
            items = sale.get("items", [])
            formatted_items = format_items(items)
            df = pd.DataFrame(formatted_items)
            sheet_name = f"Receipt_{i+1}"
            df.to_excel(writer, sheet_name=sheet_name[:31], index=False)  # max 31 characters

    excel_data = output.getvalue()
    b64 = base64.b64encode(excel_data).decode()
    href = f'<a download="sales_history.xlsx" href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}" target="_blank">Click here to download Excel</a>'
    st.markdown(href, unsafe_allow_html=True)

def export_to_pdf(sales):
    """Export all sales to PDF file"""
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    styles = getSampleStyleSheet()
    elements = []

    for sale in sales:
        elements.append(Paragraph(f"Receipt ID: {sale['_id']}", styles["Normal"]))
        elements.append(Paragraph(f"Customer: {sale['customer_name']}", styles["Normal"]))
        elements.append(Paragraph(f"Phone: {sale['phone']}", styles["Normal"]))
        elements.append(Paragraph(f"Date: {sale['created_at']}", styles["Normal"]))
        elements.append(Spacer(1, 0.2*inch))

        items = sale.get("items", [])
        formatted_items = format_items(items)
        if formatted_items:
            df = pd.DataFrame(formatted_items)
            data = [["Code", "Name", "Qty", "Price", "Total"]]
            for _, row in df.iterrows():
                line_total = row["qty"] * row["price"]
                data.append([row["code"], row["name"], row["qty"], f"{row['price']:.2f}", f"{line_total:.2f}"])
            
            table = Table(data)
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), '#cceeff'),
                ('TEXTCOLOR', (0, 0), (-1, 0), '#000000'),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTSIZE', (0, 0), (-1, 0), 12),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), '#f7f7f7'),
                ('GRID', (0, 0), (-1, -1), 1, '#000000')
            ]))
            elements.append(table)
            elements.append(Spacer(1, 0.5*inch))

    doc.build(elements)

    pdf_data = buffer.getvalue()
    buffer.close()

    b64 = base64.b64encode(pdf_data).decode()
    href = f'<a download="sales_history.pdf" href="data:application/pdf;base64,{b64}" target="_blank">Click here to download PDF</a>'
    st.markdown(href, unsafe_allow_html=True)