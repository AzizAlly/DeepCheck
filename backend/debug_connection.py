import socket
import ssl
import certifi
from pymongo import MongoClient
import urllib.parse

print("="*60)
print("MongoDB Connection Debug")
print("="*60)

# Your credentials
username = "aziz45_db_user"
password = "@zz1@l|y"  # Original password
encoded_password = urllib.parse.quote_plus(password)

print(f"Username: {username}")
print(f"Password encoded: {encoded_password}")

# Try different connection formats
formats = [
    {
        "name": "Standard SRV",
        "uri": f"mongodb+srv://{username}:{encoded_password}@cluster0.ij6amg8.mongodb.net/deepcheck?retryWrites=true&w=majority"
    },
    {
        "name": "Without SRV (direct)",
        "uri": f"mongodb://{username}:{encoded_password}@ac-szchfl0-shard-00-00.ij6amg8.mongodb.net:27017,ac-szchfl0-shard-00-01.ij6amg8.mongodb.net:27017,ac-szchfl0-shard-00-02.ij6amg8.mongodb.net:27017/deepcheck?ssl=true&replicaSet=atlas-14i9fd-shard-0&authSource=admin&retryWrites=true"
    },
    {
        "name": "With SSL disabled (testing only)",
        "uri": f"mongodb+srv://{username}:{encoded_password}@cluster0.ij6amg8.mongodb.net/deepcheck?retryWrites=true&w=majority&ssl=false"
    }
]

for fmt in formats:
    print(f"\n🔄 Testing: {fmt['name']}")
    try:
        client = MongoClient(
            fmt['uri'],
            serverSelectionTimeoutMS=5000,
            tlsAllowInvalidCertificates=True,
            tlsAllowInvalidHostnames=True
        )
        client.admin.command('ping')
        print("✅ SUCCESS!")
        
        db = client.deepcheck
        print(f"Collections: {db.list_collection_names()}")
        break
    except Exception as e:
        print(f"❌ Failed: {e}")
