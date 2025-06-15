def show_printer():
    import streamlit as st
    from components.header import render_header
    from utils.connection import get_remains_with_details, get_sales_collection, get_remain_collection
    from datetime import datetime

    remain_collection = get_remains_with_details()
    sales_collection = get_sales_collection()
    rm_collection = get_remain_collection()

    render_header()
    st.title("📄 Invoice / Voucher Preview")

    col11, col22 = st.columns(2)

    with col11:
        # Customer Info
        customer_name = st.text_input("Customer Name", key="customer_name")
        phone = st.text_input("Phone Number", key="phone")

        # Items Table
        num_items = st.number_input("Number of Items", min_value=1, value=st.session_state.get("num_items", 1), key="num_items")

        items = []
        total_amount = 0.0

        for i in range(num_items):
            col0, col1, col2, col3 = st.columns(4)

            with col0:
                code = st.text_input(f"Code {i+1}", key=f"code_{i}")
            
            item_data = None
            if code:
                item_data = next((item for item in remain_collection if item["code"] == code), None)

            with col1:
                name = st.text_input(
                    f"Item {i+1} Name",
                    value=item_data["item_name"] if item_data and "item_name" in item_data else "",
                    key=f"name_{i}",
                    disabled=True
                )

            with col2:
                qty = st.number_input(f"Qty", min_value=1, key=f"qty_{i}")

            with col3:
                price = st.number_input(
                    f"Price",
                    min_value=0.0,
                    format="%.2f",
                    value=item_data["remain_price"] if item_data and "remain_price" in item_data else 0.0,
                    key=f"price_{i}",
                    disabled=True
                )

            line_total = qty * price
            total_amount += line_total

            if code and name and qty and price:
                items.append({
                    "code": code,
                    "name": name,
                    "qty": qty,
                    "price": price
                })

    with col22:
        if st.button("Sales", type="primary", use_container_width=True):
            if not items:
                st.warning("No valid items to save.")
            elif not customer_name or not phone:
                st.warning("Please enter customer name and phone number.")
            else:
                sale_data = {
                    "customer_name": customer_name,
                    "phone": phone,
                    "items": items,
                    "total_amount": total_amount,
                    "created_at": datetime.now()
                }

                # Save to sales collection
                sales_collection.insert_one(sale_data)

                # Update remains collection
                for item in items:
                    rm_collection.update_one(
                        {"code": item["code"]},
                        {"$inc": {"remain_stock": -int(item["qty"])}}
                    )

                # Clear all fields
                for key in ["customer_name", "phone", "num_items"]:
                    if key in st.session_state:
                        del st.session_state[key]

               # Item fields တွေဖျက်
                for i in range(num_items):
                    for field in ["code_", "name_", "qty_", "price_"]:
                        key = f"{field}{i}"
                        if key in st.session_state:
                            del st.session_state[key]

                st.success("Sale recorded successfully!")
                st.rerun()

        st.divider()

        if customer_name and phone and len(items) > 0:
            from utils.printer_utils import render_voucher
            html_voucher = render_voucher(customer_name, phone, items)
            st.html(html_voucher)
        else:
            st.warning("Please fill all fields to see the voucher preview.")