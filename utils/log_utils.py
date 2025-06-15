from datetime import datetime
from utils.connection import get_log_collection

def add_log(user, action, description, ref_id=None):
    """
    Activity log တွေကို database ထဲသို့သိမ်း
    """
    log_collection = get_log_collection()

    log_data = {
        "user": user,
        "action": action,
        "description": description,
        "timestamp": datetime.now(),
    }

    if ref_id:
        log_data["ref_id"] = ref_id

    log_collection.insert_one(log_data)