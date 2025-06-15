# create.py

import streamlit as st
from utils.connection import get_item_collection,get_supplier_collection,get_category_collection,get_remain_collection
from components.header import render_header
from components.footer import render_footer
from bson.objectid import ObjectId
from datetime import datetime

def remain_insert(code, qty, price):
    """
    code ကိုကြည့်ပြီး remains table ထဲမှာ qty ပေါင်းသွင်း သို့မဟုတ် အသစ်ထည့်
    """
    remain_collection = get_remain_collection()

    # Query filter
    query = {
        "code": code
    }

    # Update operation
    update = {
        "$inc": {
            "remain_stock": qty
        },
        "$set": {
            "remain_price": price,  # တန်ဖိုးကိုအမြဲတမ်းသိမ်း
        },
        "$setOnInsert": {
            "create_at": datetime.now()
        }
    }
    # Upsert operation (Update သို့မဟုတ် Insert)
    remain_collection.update_one(query, update, upsert=True)
    
def show():
    render_header()

    item_collection = get_item_collection()
    category_collection = get_category_collection()
    supplier_collection = get_supplier_collection()    

    st.title("Create Item")

    with st.form("create",clear_on_submit=False,  enter_to_submit=True, ):
        code = st.text_input("Code",key="code")

        # Auto-fetch item by code if exists
        item_data = None
        if code:
            item_data = item_collection.find_one({"code": code})

        name = st.text_input("Name", key="name",value=item_data["name"] if item_data and "name" in item_data else "")
        qty = st.number_input("Quantity",key="qty", min_value=1, value=int(item_data["qty"]) if item_data and "qty" in item_data else 1)
        price = st.number_input("Price",key="price", min_value=0.0, format="%.2f", value=float(item_data["price"]) if item_data and "price" in item_data else 0.0)

        # Category dropdown
        categories = list(category_collection.find())
        category_options = {str(cat["_id"]): cat["name"] for cat in categories}
        selected_category_id = st.selectbox(
            "Select Category",
            options=category_options.keys(),
            format_func=lambda x: category_options[x],
            index= list(category_options.keys()).index(str(item_data["category_id"])) if item_data and "category_id" in item_data else 0
        )

        # Supplier dropdown
        suppliers = list(supplier_collection.find())
        supplier_options = {str(sup["_id"]): sup["name"] for sup in suppliers}
        selected_supplier_id = st.selectbox(
            "Select Supplier",
            options=supplier_options.keys(),
            format_func=lambda x: supplier_options[x],
            index= list(supplier_options.keys()).index(str(item_data["supplier_id"])) if item_data and "supplier_id" in item_data else 0
        )


        col=st.columns(3,gap="small")

        if col[0].form_submit_button("Add Item" , type="primary",use_container_width=True):
            if name and qty > 0 and price >= 0:
                result=item_collection.insert_one({
                    "code":code,
                    "name": name,
                    "qty": qty,
                    "price": price,
                    "category_id": ObjectId(selected_category_id),
                    "supplier_id": ObjectId(selected_supplier_id),
                    "created_at": datetime.now()  # သို့မဟုတ် MongoDB ကပေးချင်ရင်မထည့်ပါနဲ့
                })

                remain_insert(code,qty,price)
                
                st.success(f"Item {name} added successfully!")
                st.rerun()
            else:
                st.warning("Please fill both fields.")
        if col[1].form_submit_button("Show Item",type="primary",use_container_width=True):
            st.session_state.page="show_item"
            st.rerun()

    render_footer()