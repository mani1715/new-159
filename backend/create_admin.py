#!/usr/bin/env python3
"""
Script to create admin user in the database
"""
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from auth import hash_password
import uuid
from datetime import datetime

async def create_admin_user():
    # Connect to MongoDB
    client = AsyncIOMotorClient('mongodb://localhost:27017')
    db = client['test_database']
    users_collection = db['users']
    
    # Check if admin already exists
    existing_admin = await users_collection.find_one({"email": "admin@mspn.com"})
    
    if existing_admin:
        print("Admin user already exists!")
        print(f"Email: {existing_admin['email']}")
        client.close()
        return
    
    # Create admin user
    admin_user = {
        "id": str(uuid.uuid4()),
        "name": "Admin",
        "email": "admin@mspn.com",
        "password_hash": hash_password("admin123"),
        "role": "admin",
        "created_at": datetime.utcnow().isoformat()
    }
    
    await users_collection.insert_one(admin_user)
    print("✅ Admin user created successfully!")
    print(f"Email: admin@mspn.com")
    print(f"Password: admin123")
    print("\n⚠️  Please change this password after first login!")
    
    client.close()

if __name__ == "__main__":
    asyncio.run(create_admin_user())
