def show():
    import streamlit as st
    from utils.connection import get_log_collection
    import pandas as pd
    from datetime import datetime

    log_collection = get_log_collection()
    
    st.title("🧾 Activity Logs")

    # Filter Options
    col1, col2 = st.columns(2)
    with col1:
        user_filter = st.text_input("Filter by User")
    with col2:
        date_filter = st.date_input("Filter by Date", value=None)

    # Fetch logs
    logs = list(log_collection.find().sort("timestamp", -1))

    filtered_logs = []
    for log in logs:
        match = True
        if user_filter and user_filter.lower() not in log.get("user", "").lower():
            match = False
        if date_filter and log.get("timestamp").date() != date_filter:
            match = False
        if match:
            filtered_logs.append(log)

    if not filtered_logs:
        st.info("No logs found.")
        return

    # Export Buttons
    col_export1, col_export2 = st.columns(2)
    if col_export1.button("Export to Excel"):
        export_to_excel(filtered_logs)
    if col_export2.button("Export to PDF"):
        export_to_pdf(filtered_logs)

    # Show Logs
    for log in filtered_logs:
        with st.expander(f"{log['action']} — {log.get('user', 'N/A')} — {log['timestamp'].strftime('%Y-%m-%d %H:%M')}"):
            st.markdown(f"**Description:** {log['description']}")
            if "ref_id" in log:
                st.markdown(f"**Reference ID:** {log['ref_id']}")

def export_to_excel(logs):
    df = pd.DataFrame(logs)
    df["timestamp"] = df["timestamp"].dt.strftime("%Y-%m-%d %H:%M")
    output = BytesIO()
    with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
        df.to_excel(writer, index=False, sheet_name="Logs")
    data = output.getvalue()
    b64 = base64.b64encode(data).decode()
    href = f'<a download="activity_logs.xlsx" href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}">Download Excel</a>'
    st.markdown(href, unsafe_allow_html=True)

def export_to_pdf(logs):
    from io import BytesIO
    from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
    from reportlab.lib.styles import getSampleStyleSheet
    from reportlab.lib.pagesizes import letter
    from reportlab.pdfbase.ttfonts import TTFont
    from reportlab.pdfbase import pdfmetrics
    import base64

    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    styles = getSampleStyleSheet()
    style_normal = styles["Normal"]

    # Register Myanmar Font
    pdfmetrics.registerFont(TTFont("Padauk", "fonts/Padauk.ttf"))
    style_normal.fontName = "Padauk"
    style_normal.fontSize = 12

    elements = []

    for log in logs:
        timestamp = log["timestamp"].strftime("%Y-%m-%d %H:%M")
        elements.append(Paragraph(f"<font name='Padauk'>User: {log.get('user', '')}</font>", style_normal))
        elements.append(Paragraph(f"<font name='Padauk'>Action: {log['action']}</font>", style_normal))
        elements.append(Paragraph(f"<font name='Padauk'>Description: {log['description']}</font>", style_normal))
        elements.append(Paragraph(f"<font name='Padauk'>Time: {timestamp}</font>", style_normal))
        elements.append(Spacer(1, 0.2*inch))
        elements.append(Paragraph("-"*50, style_normal))
        elements.append(Spacer(1, 0.2*inch))

    doc.build(elements)
    pdf_data = buffer.getvalue()
    buffer.close()

    b64 = base64.b64encode(pdf_data).decode()
    href = f'<a download="activity_logs.pdf" href="data:application/pdf;base64,{b64}" target="_blank">Download PDF</a>'
    st.markdown(href, unsafe_allow_html=True)