def render_header():
    import streamlit as st

    theme = st.session_state.get("theme", "light")

    bg_color = "#ffffff" if theme == "light" else "#1f1f1f"
    text_color = "#000000" if theme == "light" else "#ffffff"

    st.markdown(f"""
    <style>
    .header {{
        background-color: {bg_color};
        color: {text_color};
        padding: 1em;
        text-align: center;
        font-size: 1.8em;
        border-bottom: 1px solid #ddd;
    }}
    </style>
    """, unsafe_allow_html=True)

    st.markdown('<div class="header">My Streamlit App</div>', unsafe_allow_html=True)