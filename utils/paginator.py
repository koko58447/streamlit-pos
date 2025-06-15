def paginate_dataframe(df, rows_per_page=5):
    """
    DataFrame ကို pagination နဲ့ပြပေးတဲ့ function
    """
    import streamlit as st
    import pandas as pd

    total_rows = len(df)
    total_pages = (total_rows // rows_per_page) + (1 if total_rows % rows_per_page > 0 else 0)

    if "current_page" not in st.session_state:
        st.session_state.current_page = 1

    current_page = st.session_state.current_page

    start_idx = (current_page - 1) * rows_per_page
    end_idx = start_idx + rows_per_page
    page_df = df.iloc[start_idx:end_idx]

    st.markdown(f"### Page {current_page} of {total_pages}")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col1:
        if st.button("⬅️"):
            st.session_state.current_page = max(1, current_page - 1)
    with col2:
        if st.button("➡️"):
            st.session_state.current_page = min(total_pages, current_page + 1)

    st.dataframe(page_df, use_container_width=True)

    return page_df