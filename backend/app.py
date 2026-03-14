from fastapi import FastAPI, HTTPException, Depends, status, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import datetime, timedelta
from typing import Optional
import os
import shutil
from pathlib import Path

# Import database
from database.config import db, client

# Import model
from model import predict_video

print(f"""
{'='*60}
DeepCheck - Deepfake Detection System
Author: Aziz Ali
Email: alyyaziz45@gmail.com
Supervisor: Mr. Hassan
University: KIUT
{'='*60}
""")

# Initialize FastAPI
app = FastAPI(
    title="DeepCheck API",
    description="Deepfake Detection System - KIUT Computer Science Project",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create temp directory for uploads
UPLOAD_DIR = Path("temp_uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

# ============================================================
#  Health Check Endpoint
# ============================================================
@app.get("/health")
async def health_check():
    """Check if API is running and database is connected"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "database": "connected" if db is not None else "disconnected",
        "student": "Aziz Ali",
        "supervisor": "Mr. Hassan",
        "university": "KIUT"
    }

# ============================================================
#  Database Stats Endpoint
# ============================================================
@app.get("/admin/db-stats")
async def database_stats():
    """Get database statistics"""
    if db is None:
        return {
            "status": "error",
            "message": "Database not connected",
            "student": "Aziz Ali",
            "supervisor": "Mr. Hassan",
            "university": "KIUT"
        }
    
    try:
        collections = db.list_collection_names()
        stats = {
            "status": "connected",
            "database": db.name,
            "student": "Aziz Ali",
            "supervisor": "Mr. Hassan",
            "university": "KIUT",
            "timestamp": datetime.now().isoformat(),
            "collections": {}
        }
        
        for coll_name in collections:
            count = db[coll_name].count_documents({})
            stats["collections"][coll_name] = {
                "document_count": count
            }
        
        return stats
    except Exception as e:
        return {"status": "error", "message": str(e)}

# ============================================================
#  Predictions Endpoint
# ============================================================
@app.get("/predictions")
async def get_predictions():
    """Get all predictions from database"""
    if db is None:
        return {"status": "error", "message": "Database not connected"}
    
    try:
        predictions = list(db.predictions.find({}, {'_id': 0}).sort("created_at", -1))
        return {
            "status": "success",
            "count": len(predictions),
            "predictions": predictions
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}

# ============================================================
#  User Registration Endpoint (JSON Body)
# ============================================================
@app.post("/auth/register")
async def register_user(user: dict):
    """Register a new user (expects JSON body)"""
    if db is None:
        return {"status": "error", "message": "Database not connected"}
    
    try:
        # Extract data from JSON body
        username = user.get("username")
        email = user.get("email")
        password = user.get("password")
        
        if not username or not email or not password:
            return {"status": "error", "message": "Missing required fields: username, email, password"}
        
        # Check if user exists
        existing = db.users.find_one({"username": username})
        if existing:
            return {"status": "error", "message": "Username already exists"}
        
        # Create user
        new_user = {
            "username": username,
            "email": email,
            "password": password,  # In production, hash this!
            "created_at": datetime.now().isoformat()
        }
        
        result = db.users.insert_one(new_user)
        return {
            "status": "success",
            "message": "User created successfully",
            "username": username,
            "email": email
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}

# ============================================================
#  Login Endpoint
# ============================================================
@app.post("/auth/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """Login user with OAuth2 form data"""
    if db is None:
        return {"status": "error", "message": "Database not connected"}
    
    try:
        username = form_data.username
        password = form_data.password
        
        user = db.users.find_one({"username": username, "password": password})
        if user:
            return {
                "status": "success",
                "access_token": "demo_token_" + username,
                "token_type": "bearer",
                "username": username
            }
        else:
            return {"status": "error", "message": "Invalid credentials"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

# ============================================================
#  Predict Endpoint
# ============================================================
@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    """Upload video for deepfake detection"""
    if not file.filename.endswith(('.mp4', '.avi', '.mov', '.mkv')):
        raise HTTPException(400, "File must be a video")
    
    file_path = UPLOAD_DIR / file.filename
    
    try:
        # Save file
        with file_path.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # Make prediction
        label, confidence = predict_video(str(file_path))
        
        # Save to database if connected
        if db is not None:
            prediction = {
                "filename": file.filename,
                "prediction": label,
                "confidence": confidence,
                "is_fake": label == "FAKE",
                "created_at": datetime.now().isoformat()
            }
            db.predictions.insert_one(prediction)
        
        return {
            "filename": file.filename,
            "prediction": label,
            "confidence": confidence,
            "is_fake": label == "FAKE"
        }
    finally:
        # Cleanup
        if file_path.exists():
            file_path.unlink()

# ============================================================
#  Home Endpoint
# ============================================================
@app.get("/")
async def home():
    return {
        "message": "DeepCheck API is running",
        "student": "Aziz Ali",
        "supervisor": "Mr. Hassan",
        "university": "KIUT",
        "endpoints": [
            "/health",
            "/admin/db-stats", 
            "/predictions",
            "/auth/register",
            "/auth/login",
            "/predict"
        ]
    }
