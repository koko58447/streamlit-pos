def show_modal(title, content):
    import streamlit as st

    st.markdown(f"""
    <style>
    .modal {{
        display: none; /* Hidden by default */
        position: fixed;
        z-index: 999;
        padding-top: 60px;
        left: 0;
        top: 0;
        width: 100%;
        height: 100%;
        overflow: auto;
        background-color: rgba(0,0,0,0.4);
    }}
    .modal-content {{
        background-color: #fff;
        margin: 5% auto;
        padding: 20px;
        border: 1px solid #888;
        width: 70%;
        border-radius: 10px;
    }}
    .close {{
        color: #aaa;
        float: right;
        font-size: 28px;
        font-weight: bold;
        cursor: pointer;
    }}
    .close:hover {{
        color: black;
    }}
    </style>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div id="myModal" class="modal">
      <div class="modal-content">
        <span class="close" onclick="document.getElementById('myModal').style.display='none'">&times;</span>
        <h2>{title}</h2>
        <p>{content}</p>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # JavaScript to show modal when button is clicked
    st.markdown("""
    <script>
    const btn = document.querySelector('[data-modal-trigger]');
    if (btn) {
        btn.addEventListener('click', () => {
            document.getElementById('myModal').style.display = 'block';
        });
    }
    </script>
    """, unsafe_allow_html=True)