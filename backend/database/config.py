import os
from pymongo import MongoClient
import logging
import certifi
from datetime import datetime

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

print(f"""
╔{'═'*58}╗
║{' '*58}║
║{'DeepCheck - Database Connected!':^58}║
║{' '*58}║
╠{'═'*58}╣
║ Student: Aziz Ali{' '*(41)}║
║ Supervisor: Mr. Hassan{' '*(34)}║
║ University: KIUT{' '*(37)}║
╚{'═'*58}╝
""")

# MongoDB connection string
MONGO_URL = 'mongodb+srv://aziz45_db_user:%40zz1%40l%7Cy@cluster0.ij6amg8.mongodb.net/deepcheck?retryWrites=true&w=majority&tls=true&tlsAllowInvalidCertificates=true&tlsAllowInvalidHostnames=true'

# Initialize database as global
client = None
db = None

try:
    logger.info('Connecting to MongoDB Atlas...')
    
    # Create client
    client = MongoClient(
        MONGO_URL,
        serverSelectionTimeoutMS=5000
    )
    
    # Test connection
    client.admin.command('ping')
    logger.info('✅ Connected to MongoDB!')
    
    # Set database
    db = client['deepcheck']
    logger.info(f'📊 Database: {db.name}')
    
    # Show collections
    collections = db.list_collection_names()
    logger.info(f'📚 Collections: {collections}')
    
    # Show counts
    if 'users' in collections:
        user_count = db.users.count_documents({})
        logger.info(f'👤 Users: {user_count}')
    
    if 'predictions' in collections:
        pred_count = db.predictions.count_documents({})
        logger.info(f'🎥 Predictions: {pred_count}')
    
    logger.info('✅ Database ready!')
    
except Exception as e:
    logger.error(f'❌ Connection failed: {e}')
    client = None
    db = None

# Export db and client
__all__ = ['db', 'client']
