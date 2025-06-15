def show_product():
    import streamlit as st
    from components.header import render_header
    from utils.paginator import paginate_dataframe
    import pandas as pd

    render_header()
   # Sample Data
    data = {
        "ID": range(1, 101),
        "Name": [f"User {i}" for i in range(1, 101)],
        "Email": [f"user{i}@example.com" for i in range(1, 101)],
        "Age": [20 + i % 30 for i in range(1, 101)]
    }

    df = pd.DataFrame(data)

   # Rows per page selector
    rows_per_page = st.selectbox("Rows per page", options=[5, 10, 20, 50], index=1)

    # Paginate and show
    paginate_dataframe(df, rows_per_page=rows_per_page)
