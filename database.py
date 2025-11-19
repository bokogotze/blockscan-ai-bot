from pymongo import MongoClient
import os
from datetime import datetime, timedelta

MONGO_URI = os.getenv("MONGO_URI")

client = MongoClient(MONGO_URI)
db = client["blockscan"]
users = db["users"]

def get_user(user_id):
    return users.find_one({"user_id": user_id})

def create_user(user_id):
    if not get_user(user_id):
        users.insert_one({
            "user_id": user_id,
            "premium": False,
            "expiry": None,
            "trial_used": False
        })

def set_premium(user_id, days):
    expiry = datetime.utcnow() + timedelta(days=days)
    users.update_one(
        {"user_id": user_id},
        {"$set": {"premium": True, "expiry": expiry}},
        upsert=True
    )

def is_premium(user_id):
    user = get_user(user_id)
    if not user or not user.get("expiry"):
        return False
    return user["expiry"] > datetime.utcnow()

def set_trial_used(user_id):
    users.update_one(
        {"user_id": user_id},
        {"$set": {"trial_used": True}},
        upsert=True
    )

def has_used_trial(user_id):
    user = get_user(user_id)
    if not user:
        return False
    return user.get("trial_used", False)
