def render_left_nav_bar(text):
    import streamlit as st

    #### page title , logo ချိန်းရန်

    st.set_page_config(
        page_title="Master Template",
        page_icon="🧊",
        layout="wide",
        initial_sidebar_state="expanded",
        menu_items={
            'Get Help': 'https://www.extremelycoolapp.com/help',
            'Report a bug': "https://www.extremelycoolapp.com/bug",
            'About': "# This is a header. This is an *extremely* cool app!"
        }
    )

    current_page = st.session_state.get("page", "home")
    role = st.session_state.get("role", "user")
    lang = st.session_state.get("language", "en")

     # Sidebar မှာ logo ကို center ပြပေးတဲ့ styling
    st.markdown("""
    <style>
        .sidebar .sidebar-content {
            display: flex;
            flex-direction: column;
            align-items: center;
            width: 50%;
        }
        .logo {
            margin-bottom: 20px;
        }
    </style>
    """, unsafe_allow_html=True)

    #Logo Image
    st.logo("assets/logo.png",size="large")
  
    st.sidebar.image("assets/logo2.jpg")

    # Sidebar header with logo
    st.markdown("""
    <style>
        .sidebar .sidebar-content {
            width: 100%;
            max-width: 300px;
        }
       
        .nav-button {
            background-color: #f0f0f0;
            color: #333;
            border: none;
            width: 100%;
            text-align: left;
            padding: 10px 15px;
            margin: 5px 0;
            border-radius: 8px;
            font-size: 16px;
            cursor: pointer;
            transition: all 0.2s ease;
        }
        .nav-button:hover { background-color: #e0e0e0; }
        .active {
            background-color: #d1ecf1 !important;
            color: #0c5460;
            font-weight: bold;
        }
        .sub-menu { margin-left: 20px; }
        .search-box input {
            width: 100%;
            padding: 5px;
        }
    </style>
    """, unsafe_allow_html=True)

    # Search box
    search_term = st.text_input("🔍 Search", placeholder="Search menu...", key="menu_search")

    ###### nav - bar မှာ button ထပ်ထည့်ရန်

    # Menu items with roles and icons
    menu_items = {
        text["home"]: {"key":"home" , "icon": "🏠"},
         text["about"]: {"key": "about", "icon": "ℹ️"},
         text["product"]: {"key": "product", "icon": "ℹ️"},
        "Printer Test": {"key": "printer", "icon": "🖨️"},  
         "Category": {"key": "show_category", "icon": "⚙️"},
         "Supplier": {"key": "show_supplier", "icon": "⚙️"},
         "Item": {"key": "show_item", "icon": "⚙️"},   
         "Inventory": {"key": "show_remain", "icon": "⚙️"},
         "Sale": {"key": "show_sale", "icon": "⚙️"},  
         "Sale History": {"key": "show_history", "icon": "⚙️"},       
        "CRUD" : {
            "Show": {"key": "show", "icon": "🔍"},

        },
        "Settings": {
            "User Profile": {"key": "profile", "icon": "👤"},
            "Preferences": {"key": "preferences", "icon": "⚙️"}
        },
        "Admin Tools": {
            "User Management": {"key": "user_management", "icon": "👥", "roles": ["admin"]},
            "System Logs": {"key": "system_logs", "icon": "📜", "roles": ["admin"]}
        }
    }

    # Render filtered menu
    for label, item in menu_items.items():
        if isinstance(item, dict):
            if "roles" in item and role not in item["roles"]:
                continue

            has_nested_items = any(isinstance(sub_item, dict) for sub_label, sub_item in item.items())

            if has_nested_items:
                with st.expander(f"📁 {label}"):
                    for sub_label, sub_item in item.items():
                        if not isinstance(sub_item, dict):
                            continue
                        if "roles" in sub_item and role not in sub_item["roles"]:
                            continue

                        icon = sub_item.get("icon", "")
                        btn_label = f"{icon} {sub_label}"

                        is_active = current_page == sub_item.get("key", "")
                        btn_class = "nav-button active" if is_active else "nav-button"

                        if search_term.lower() in sub_label.lower():
                            if st.button(btn_label, key=f"btn_{sub_item['key']}", use_container_width=True):
                                st.session_state.page = sub_item["key"]
            else:
                icon = item.get("icon", "")
                btn_label = f"{icon} {label}"

                is_active = current_page == item.get("key", "")
                btn_class = "nav-button active" if is_active else "nav-button"

                if search_term.lower() in label.lower():
                    if st.button(btn_label, key=f"btn_{item['key']}", use_container_width=True):
                        st.session_state.page = item["key"]

        else:
            # Fallback for plain string entries (shouldn't happen if all are dicts)
            if search_term.lower() in label.lower():
                if st.button(label, key=f"btn_{label}", use_container_width=True):
                    st.session_state.page = label.lower()

    st.markdown("---")
    st.markdown("#### 🎨 Theme")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🌞", key="btn_light", help="Switch to Light Mode"):
            st.session_state.theme = "light"
            st.rerun()
    with col2:
        if st.button("🌙", key="btn_dark", help="Switch to Dark Mode"):
            st.session_state.theme = "dark"
            st.rerun()
            
    st.markdown("---")

    st.markdown("### 🌍 Language")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🇬🇧 EN", use_container_width=True):
            st.session_state.language = "en"
            st.rerun()
    with col2:
        if st.button("🇲🇲 မြန်မာ", use_container_width=True):
            st.session_state.language = "my"
            st.rerun()
    st.write(text["language"])
    st.markdown("---")
    
    if st.button("🔓 Logout", key="btn_logout", help="Logout from your account", use_container_width=True, type="primary"):
        st.session_state.logged_in = False
        st.session_state.role = None
        st.rerun()