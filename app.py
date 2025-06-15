import streamlit as st
from utils.session_utils import initialize_session_state

# Initialize session state
initialize_session_state()

# ဘာသာစကား load လုပ်ပါ
lang_module = "en" if st.session_state.language == "en" else "my"
lang = __import__(f"lang.{lang_module}", fromlist=["texts"])
TEXTS = lang.texts

# Check login status
if not st.session_state.logged_in:
    from components.login_form import render_login_form
    render_login_form()
else:
    # Sidebar Navigation
    from components.left_nav_bar import render_left_nav_bar
    with st.sidebar:
        render_left_nav_bar(TEXTS)

    ### ဒီမှာ routes တွေထပ်ထည့်မယ်   ############

    # Page routing
    if st.session_state.page == "home":
        from my_pages.home import show_home
        show_home()
    elif st.session_state.page == "about":
        from my_pages.about import show_about
        show_about()
    elif st.session_state.page == "profile":
        from my_pages.profile import show_profile
        show_profile()
    elif st.session_state.page == "preferences":
        from my_pages.preferences import show_preferences
        show_preferences()
    elif st.session_state.page == "user_management":
        from my_pages.user_management import show_user_management
        show_user_management()
    elif st.session_state.page == "system_logs":
        from my_pages.system_logs import show_system_logs
        show_system_logs()
    elif st.session_state.page == "product":
        from my_pages.product import show_product
        show_product()
    elif st.session_state.page == "printer":
        from my_pages.printer_test import show_printer
        show_printer()
    elif st.session_state.page == "create":
        from crud.create import show_create
        show_create()
    elif st.session_state.page == "show":
        from crud.show import show_create
        show_create()
    elif st.session_state.page == "update":
        from crud.update import show_update
        show_update()
    elif st.session_state.page == "show_category":
        from category.show import show_create
        show_create()
    elif st.session_state.page == "create_category":
        from category.create import show_create
        show_create()
    elif st.session_state.page == "update_category":
        from category.update import show
        show()
    elif st.session_state.page == "show_supplier":
        from supplier.show import show
        show()
    elif st.session_state.page == "create_supplier":
        from supplier.create import show
        show()
    elif st.session_state.page == "update_supplier":
        from supplier.update import show
        show()
    elif st.session_state.page == "show_item":
        from item.show import show
        show()
    elif st.session_state.page == "create_item":
        from item.create import show
        show()
    elif st.session_state.page == "update_item":
        from item.update import show
        show()
    elif st.session_state.page == "show_remain":
        from remain.show import show
        show()
    elif st.session_state.page == "show_sale":
        from sale.sale import show
        show()
    elif st.session_state.page == "show_history":
        from sale.show import show
        show()
