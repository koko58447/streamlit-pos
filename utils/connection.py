# connection.py

from pymongo import MongoClient
from datetime import datetime

def get_db():
    client = MongoClient("mongodb://localhost:27017")  # Local MongoDB
    db = client["crud"]  # Database name
    return db

# Collection တွေကိုရယူဖို့ function တွေဖန်တီးပါမယ်
def get_user_collection():
    db = get_db()
    return db["users"]

def get_category_collection():
    db = get_db()
    category_collection = db["categories"]
    
    # လိုအပ်ရင် index တွေ create လုပ်နိုင်ပါတယ် (option)
    category_collection.create_index("name", unique=True)
    return category_collection

def get_supplier_collection():
    db = get_db()
    supplier_collection = db["suppliers"]
    
    # လိုအပ်ရင် index တွေ create လုပ်နိုင်ပါတယ် (option)
    supplier_collection.create_index("name", unique=True)
    return supplier_collection

def get_item_collection():
    db = get_db()
    item_collection = db["items"]
    return item_collection

def get_items_with_details():

    """
    items အားလုံးကို MongoDB Aggregation ဖြင့် category နဲ့ supplier နာမည်တွေနဲ့ပါ ရယူ
    """
    item_collection = get_item_collection()
    category_collection = get_category_collection()
    supplier_collection = get_supplier_collection()

    pipeline = [
        # Join with categories
        {
            "$lookup": {
                "from": "categories",
                "localField": "category_id",
                "foreignField": "_id",
                "as": "category"
            }
        },
        {
            "$addFields": {
                "category_name": {
                    "$arrayElemAt": ["$category.name", 0]
                }
            }
        },
        {
            "$project": {
                "category": 0  # category array ကိုဖျောက်ထား
            }
        },

        # Join with suppliers
        {
            "$lookup": {
                "from": "suppliers",
                "localField": "supplier_id",
                "foreignField": "_id",
                "as": "supplier"
            }
        },
        {
            "$addFields": {
               "supplier_name": {
                    "$arrayElemAt": ["$supplier.name", 0]
                },
                "supplier_email": {
                    "$arrayElemAt": ["$supplier.email", 0]
                },
                "supplier_address": {
                    "$arrayElemAt": ["$supplier.address", 0]
                }
            }
        },
        {
            "$project": {
                "supplier": 0  # supplier array ကိုဖျောက်ထား
            }
        }
    ]

    result = list(item_collection.aggregate(pipeline))
    
    return result

def get_remain_collection():
    db = get_db()
    remain_collection = db["remains"]
    
    # လိုအပ်ရင် index တွေ create လုပ်နိုင်ပါတယ် (option)
    remain_collection.create_index("code", unique=True)
    return remain_collection

def get_remains_with_details():
    """
    remains collection ကနေ item, category, supplier အသေးစိတ်ပါဝင်တဲ့ data ကို return ပြန်ပေး
    """

    # remains = get_remain_collection()
    remains = get_remain_collection()
    items = get_item_collection()
    categories = get_category_collection()
    suppliers = get_supplier_collection()

    pipeline = [
        # Join with items
        {
            "$lookup": {
                "from": "items",
                "localField": "code",
                "foreignField": "code",
                "as": "item"
            }
        },
        {
            "$addFields": {
                "item": { "$arrayElemAt": ["$item", 0] }
            }
        },

        # Join with categories
        {
            "$lookup": {
                "from": "categories",
                "localField": "item.category_id",
                "foreignField": "_id",
                "as": "category"
            }
        },
        {
            "$addFields": {
                "category": { "$arrayElemAt": ["$category", 0] }
            }
        },

        # Join with suppliers
        {
            "$lookup": {
                "from": "suppliers",
                "localField": "item.supplier_id",
                "foreignField": "_id",
                "as": "supplier"
            }
        },
        {
            "$addFields": {
                "supplier": { "$arrayElemAt": ["$supplier", 0] }
            }
        },

        # Final Fields တွေကို select
        {
            "$project": {
                "_id": 1,
                "item_id": 1,                
                "category_name": "$category.name",
                "supplier_name": "$supplier.name",
                "remain_stock": 1,
                "remain_price": 1,
                "create_at": 1,
                "item_name": "$item.name",
                "code":1
            }
        }
    ]

    result = list(remains.aggregate(pipeline))
    return result

def get_sales_collection():
    db = get_db()
    return db["sales"]

def get_logs_collection():
    db = get_db()
    return db["logs"]