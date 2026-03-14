from pymongo import MongoClient
import certifi
from datetime import datetime

# Connection string
uri = 'mongodb+srv://aziz45_db_user:%40zz1%40l%7Cy@cluster0.ij6amg8.mongodb.net/?retryWrites=true&w=majority&tls=true&tlsAllowInvalidCertificates=true&tlsAllowInvalidHostnames=true'

print("="*60)
print("DeepCheck - Database Migration")
print("="*60)
print(f"Student: Aziz Ali")
print(f"Time: {datetime.now()}")
print("="*60)

# Connect to MongoDB
client = MongoClient(uri, serverSelectionTimeoutMS=5000, tlsCAFile=certifi.where())

# Check both databases
print("\n📊 Checking databases...")
databases = client.list_database_names()
print(f"Available databases: {databases}")

if 'deepshield' in databases:
    print("\n🔍 Found deepshield database - migrating to deepcheck...")
    
    # Get source and target
    source_db = client['deepshield']
    target_db = client['deepcheck']
    
    # Copy collections from deepshield to deepcheck
    collections = source_db.list_collection_names()
    print(f"Collections to migrate: {collections}")
    
    for collection_name in collections:
        print(f"\n📋 Migrating collection: {collection_name}")
        
        # Get all documents from source
        documents = list(source_db[collection_name].find())
        print(f"   Found {len(documents)} documents")
        
        if len(documents) > 0:
            # Insert into target
            if collection_name == 'users':
                # Remove password field for safety
                for doc in documents:
                    if 'password' in doc:
                        del doc['password']
            
            result = target_db[collection_name].insert_many(documents)
            print(f"   ✅ Migrated {len(result.inserted_ids)} documents")
            
            # Verify
            new_count = target_db[collection_name].count_documents({})
            print(f"   📊 Now in deepcheck.{collection_name}: {new_count} documents")
    
    print("\n✅ Migration complete!")
    
    # Show final stats
    print("\n📊 Final Database Stats:")
    for db_name in ['deepshield', 'deepcheck']:
        if db_name in client.list_database_names():
            db = client[db_name]
            print(f"\n{db_name}:")
            for coll in db.list_collection_names():
                count = db[coll].count_documents({})
                print(f"   - {coll}: {count} documents")

else:
    print("\n✅ deepshield database not found - no migration needed")

print("\n" + "="*60)
