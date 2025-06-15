def show():
    import streamlit as st
    from utils.connection import get_remain_collection, get_sales_collection
    from datetime import datetime

    st.title("🛒 Sales Entry")

    remain_collection = get_remain_collection()
    sales_collection = get_sales_collection()

    # Customer Info
    customer_name = st.text_input("Customer Name")
    phone = st.text_input("Phone Number")

    # Sale Items
    num_items = st.number_input("Number of Items", min_value=1, value=1)
    items = []

    total_amount = 0.0

    for i in range(num_items):
        col_code, col_qty, col_price, col_total = st.columns(4)

        with col_code:
            code = st.text_input(f"Item Code {i+1}", key=f"code_{i}")

        item_data = None
        if code:
            item_data = remain_collection.find_one({"code": code})
            if not item_data:
                st.warning(f"Item with code '{code}' not found.")
        
        with col_qty:
            qty = st.number_input(f"Qty {i+1}", min_value=1, value=1, key=f"qty_{i}")
        
        with col_price:
            price = st.number_input(
                f"Price {i+1}",
                min_value=0.0,
                format="%.2f",
                value=item_data["remain_price"] if item_data else 0.0,
                key=f"price_{i}"
            )

        with col_total:
            line_total = qty * price
            st.markdown(f"<br><b>{line_total:.2f}</b>", unsafe_allow_html=True)
            total_amount += line_total

        if code and qty and price:
            items.append({
                "code": code,
                "name": item_data.get("item_name", "") if item_data else "",
                "qty": qty,
                "price": price,
                "total": line_total
            })

        st.markdown("---")

    # Show Total
    st.markdown(f"### 💵 Total Amount: `{total_amount:.2f}`")

    # Submit Button
    if st.button("Save Sale", type="primary",):
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
                remain_collection.update_one(
                    {"code": item["code"]},
                    {"$inc": {"remain_stock": -item["qty"]}}
                )

            st.success("Sale recorded successfully!")
            st.rerun()
