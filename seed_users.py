"""
Script to seed test credentials directly into MongoDB for Admin, Advisor, and Client apps.
Run with: python3 seed_users.py
"""
import os
import asyncio
from datetime import datetime
import uuid
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

load_dotenv()

MONGO_URL = os.getenv('MONGO_URL', 'mongodb://localhost:27017/sixthsense')
DB_NAME = os.getenv('DB_NAME', 'sixthsense')

# Import password hasher from auth module
from routes.auth import hash_password

async def seed():
    print(f"Connecting to MongoDB at {MONGO_URL}...")
    client = AsyncIOMotorClient(MONGO_URL, serverSelectionTimeoutMS=5000)
    db = client[DB_NAME]

    # 1. ADMIN USER
    admin_email = "admin@psychic.com"
    admin_doc = {
        "id": "admin-super-01",
        "email": admin_email,
        "password_hash": hash_password("admin123"),
        "name": "Super Admin",
        "role": "super_admin",
        "created_at": datetime.utcnow().isoformat()
    }
    await db.admins.update_one({"email": admin_email}, {"$set": admin_doc}, upsert=True)
    print("✅ Admin created: admin@psychic.com / admin123")

    # 2. ADVISOR / PSYCHIC
    advisor_email = "advisor@psychic.com"
    advisor_doc = {
        "id": "psychic-001",
        "email": advisor_email,
        "password_hash": hash_password("advisor123"),
        "name": "Luna Mystic",
        "profile_picture": "https://images.unsplash.com/photo-1544005313-94ddf0286df2",
        "specialties": ["Love & Relationships", "Tarot Cards", "Dream Analysis"],
        "reading_methods": ["Tarot", "Clairvoyance"],
        "topics": ["Love", "Career", "Life Path"],
        "languages": ["English"],
        "years_experience": 8,
        "chat_rate": 3.99,
        "phone_rate": 4.99,
        "video_rate": 5.99,
        "online_status": "online",
        "is_online": True,
        "total_earnings": 12450.00,
        "balance": 500.0,
        "average_rating": 4.92,
        "total_reviews": 342,
        "total_readings": 1205,
        "status": "approved",
        "created_at": datetime.utcnow()
    }
    await db.psychics.update_one({"email": advisor_email}, {"$set": advisor_doc}, upsert=True)
    print("✅ Advisor created: advisor@psychic.com / advisor123")

    # 3. CLIENT / REGULAR USER
    user_email = "user@example.com"
    user_doc = {
        "id": "user-client-001",
        "email": user_email,
        "name": "John Doe",
        "password_hash": hash_password("user123"),
        "birth_date": "1995-05-15",
        "zodiac_sign": "Taurus",
        "balance": 50.0,
        "status": "active",
        "is_new_user": False,
        "first_reading_free_used": False,
        "total_spent": 0.0,
        "spending_progress": 0.0,
        "free_minutes_earned": 0,
        "free_minutes_available": 0,
        "saved_payment_methods": [],
        "created_at": datetime.utcnow()
    }
    await db.users.update_one({"email": user_email}, {"$set": user_doc}, upsert=True)
    print("✅ Client User created: user@example.com / user123")

    print("\n🎉 All credentials successfully seeded into database!")

if __name__ == "__main__":
    asyncio.run(seed())
