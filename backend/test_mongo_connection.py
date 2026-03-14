import certifi
import ssl
from pymongo import MongoClient
import urllib.parse

print("="*60)
print("DeepCheck - MongoDB Connection Test")
print("="*60)

# Connection string
uri = 'mongodb+srv://aziz45_db_user:%40zz1%40l%7Cy@cluster0.ij6amg8.mongodb.net/deepcheck?retryWrites=true&w=majority'

print(f"Connecting to: cluster0.ij6amg8.mongodb.net")
print(f"Database: deepcheck")
print(f"Certifi path: {certifi.where()}")
print("="*60)

try:
    print("\n🔄 Attempting connection...")
    client = MongoClient(
        uri,
        serverSelectionTimeoutMS=10000,
        tlsCAFile=certifi.where()
    )
    client.admin.command('ping')
    print("✅ CONNECTION SUCCESSFUL!")
    
    db = client.deepcheck
    print(f"📊 Collections: {db.list_collection_names()}")
    
except Exception as e:
    print(f"❌ Connection failed: {e}")
    
    print("\n🔄 Trying alternative method...")
    try:
        client = MongoClient(
            uri,
            serverSelectionTimeoutMS=10000,
            tls=True,
            tlsAllowInvalidCertificates=True
        )
        client.admin.command('ping')
        print("✅ CONNECTION SUCCESSFUL (relaxed SSL)!")
        
        db = client.deepcheck
        print(f"📊 Collections: {db.list_collection_names()}")
        
    except Exception as e2:
        print(f"❌ Still failed: {e2}")
