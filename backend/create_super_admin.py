#!/usr/bin/env python3
"""
Script to create super admin in the admins collection
"""
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from auth import hash_password
import uuid
from datetime import datetime

async def create_super_admin():
    # Connect to MongoDB
    client = AsyncIOMotorClient('mongodb://localhost:27017')
    db = client['test_database']
    admins_collection = db['admins']
    
    # Check if admin already exists
    existing_admin = await admins_collection.find_one({"username": "admin"})
    
    if existing_admin:
        print("Super admin already exists!")
        print(f"Username: {existing_admin['username']}")
        client.close()
        return
    
    # Create super admin
    admin_user = {
        "id": str(uuid.uuid4()),
        "username": "admin",
        "password_hash": hash_password("admin123"),
        "role": "super_admin",
        "permissions": {
            "canManageAdmins": True,
            "canViewPrivateProjects": True,
            "canAccessPrivateStorage": True,
            "canAccessChat": True
        },
        "created_at": datetime.utcnow().isoformat(),
        "created_by": "system"
    }
    
    await admins_collection.insert_one(admin_user)
    print("✅ Super admin created successfully!")
    print(f"Username: admin")
    print(f"Password: admin123")
    print("\n⚠️  Please change this password after first login!")
    
    client.close()

if __name__ == "__main__":
    asyncio.run(create_super_admin())
