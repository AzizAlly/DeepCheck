#!/usr/bin/env python
# DeepCheck Database Demo Script
# For demonstration to Mr. Hassan

import os
import sys
from datetime import datetime
from pymongo import MongoClient
from dotenv import load_dotenv

# Load environment variables
load_dotenv('database/.env')

# Project Info
print("=" * 60)
print("DEEPCHECK - DATABASE CONNECTIVITY DEMO")
print("=" * 60)
print(f"Student: Aziz Ali")
print(f"University: KIUT")
print(f"Program: Computer Science")
print(f"Supervisor: Mr. Hassan")
print(f"Time: {datetime.now()}")
print("=" * 60)

# Connect to MongoDB
print("\n📡 Connecting to MongoDB Atlas...")
mongo_url = os.getenv('MONGO_URL')

try:
    client = MongoClient(mongo_url, serverSelectionTimeoutMS=5000)
    client.admin.command('ping')
    print("✅ SUCCESS: Connected to MongoDB Atlas!")
    
    # Get database
    db = client['deepcheck']
    print(f"📊 Database: {db.name}")
    
    # Show collections
    print("\n📚 Collections:")
    collections = db.list_collection_names()
    for coll in collections:
        count = db[coll].count_documents({})
        print(f"   • {coll}: {count} documents")
    
    # If no data, create sample data
    if db.users.count_documents({}) == 0:
        print("\n🔄 Creating sample data for demonstration...")
        
        # Create a test user
        test_user = {
            "username": "demo_user",
            "email": "demo@kiut.ac.tz",
            "created_at": datetime.now(),
            "demo": True
        }
        db.users.insert_one(test_user)
        print("   ✅ Created demo user")
        
        # Create sample prediction
        sample_pred = {
            "username": "demo_user",
            "filename": "sample_video.mp4",
            "prediction": "FAKE",
            "confidence": 0.87,
            "created_at": datetime.now(),
            "demo": True
        }
        db.predictions.insert_one(sample_pred)
        print("   ✅ Created sample prediction")
    
    # Show final stats
    print("\n📈 Final Database Stats:")
    print(f"   • Users: {db.users.count_documents({})}")
    print(f"   • Predictions: {db.predictions.count_documents({})}")
    
    # Show sample data
    print("\n🔍 Sample User:")
    user = db.users.find_one()
    if user:
        print(f"   • Username: {user.get('username')}")
        print(f"   • Email: {user.get('email')}")
        print(f"   • Created: {user.get('created_at')}")
    
    print("\n🔍 Sample Prediction:")
    pred = db.predictions.find_one()
    if pred:
        print(f"   • Filename: {pred.get('filename')}")
        print(f"   • Result: {pred.get('prediction')}")
        print(f"   • Confidence: {pred.get('confidence')}")
    
    print("\n" + "=" * 60)
    print("✅ DEMO COMPLETE - Database is working!")
    print("=" * 60)
    
except Exception as e:
    print(f"❌ ERROR: {e}")
    sys.exit(1)
