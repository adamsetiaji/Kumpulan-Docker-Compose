import os
import json
import uuid
import redis
import datetime
import asyncio
from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize FastAPI
app = FastAPI(title="User Management API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Redis connection
redis_client = redis.Redis(
    host=os.getenv("REDIS_HOST", "localhost"),
    port=int(os.getenv("REDIS_PORT", 6379)),
    password=os.getenv("REDIS_PASSWORD", ""),
    db=int(os.getenv("REDIS_DB", 0)),
    decode_responses=True
)

# Models
class UserCreate(BaseModel):
    name: str
    email: str
    password: str

class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None
    balance: Optional[float] = None
    password_surfebe: Optional[str] = None
    cookie_surfebe: Optional[str] = None
    secret2fa_surfebe: Optional[str] = None
    userid_surfebe: Optional[str] = None
    balance_surfebe: Optional[float] = None
    is_register_surfebe: Optional[int] = None
    is_login_surfebe: Optional[int] = None
    payeer_account: Optional[str] = None
    payeer_password: Optional[str] = None
    payeer_master_key: Optional[str] = None
    payeer_secret_key: Optional[str] = None
    payeer_balance: Optional[float] = None
    payeer_cookie: Optional[str] = None
    is_register_payeer: Optional[int] = None
    is_login_payeer: Optional[int] = None
    is_running: Optional[int] = None
    message: Optional[str] = None

class UserBulkCreate(BaseModel):
    data: List[UserUpdate]

class UserQuery(BaseModel):
    email: str

# Generate a unique ID based on timestamp
def generate_id():
    now = datetime.datetime.now()
    return now.strftime("%Y%m%d%H%M")

# Utility function to create a new user
def create_user_record(user_data):
    user_id = generate_id()
    user_uuid = str(uuid.uuid4())
    now = datetime.datetime.now(datetime.timezone.utc).isoformat()
    
    # Set common password fields
    password = user_data.get("password", "")
    
    user = {
        "id": user_id,
        "uuid": user_uuid,
        "name": user_data.get("name", ""),
        "email": user_data.get("email", ""),
        "password": password,
        "balance": user_data.get("balance", 0),
        "password_surfebe": user_data.get("password_surfebe", password),
        "cookie_surfebe": user_data.get("cookie_surfebe", ""),
        "secret2fa_surfebe": user_data.get("secret2fa_surfebe", ""),
        "userid_surfebe": user_data.get("userid_surfebe", ""),
        "balance_surfebe": user_data.get("balance_surfebe", 0),
        "is_register_surfebe": user_data.get("is_register_surfebe", 0),
        "is_login_surfebe": user_data.get("is_login_surfebe", 0),
        "payeer_account": user_data.get("payeer_account", ""),
        "payeer_password": user_data.get("payeer_password", password),
        "payeer_master_key": user_data.get("payeer_master_key", ""),
        "payeer_secret_key": user_data.get("payeer_secret_key", ""),
        "payeer_balance": user_data.get("payeer_balance", 0),
        "payeer_cookie": user_data.get("payeer_cookie", ""),
        "is_register_payeer": user_data.get("is_register_payeer", 0),
        "is_login_payeer": user_data.get("is_login_payeer", 0),
        "is_running": user_data.get("is_running", 0),
        "message": user_data.get("message", ""),
        "created_at": now,
        "updated_at": now
    }
    
    return user

# Routes
@app.post("/api/users/create")
async def create_user(user: UserCreate):
    # Check if user already exists
    if redis_client.exists(f"user:{user.email}"):
        raise HTTPException(status_code=400, detail="User with this email already exists")
    
    user_data = {
        "name": user.name,
        "email": user.email,
        "password": user.password
    }
    
    # Create user record
    new_user = create_user_record(user_data)
    
    # Store in Redis
    redis_client.set(f"user:{user.email}", json.dumps(new_user))
    
    # Add email to user list for quick access
    redis_client.sadd("users", user.email)
    
    return {"status": "success", "data": new_user}

@app.post("/api/users/get")
async def get_user(user_query: UserQuery):
    # Get user by email
    user_data = redis_client.get(f"user:{user_query.email}")
    
    if not user_data:
        raise HTTPException(status_code=404, detail="User not found")
    
    return {"status": "success", "data": json.loads(user_data)}

@app.get("/api/users")
async def get_all_users():
    # Get all user emails
    user_emails = redis_client.smembers("users")
    users = []
    
    # Get user data for each email
    for email in user_emails:
        user_data = redis_client.get(f"user:{email}")
        if user_data:
            users.append(json.loads(user_data))
    
    return {"status": "success", "data": users}

@app.post("/api/users/update")
async def update_user(user_query: UserQuery, user_update: UserUpdate):
    # Get user by email
    user_data = redis_client.get(f"user:{user_query.email}")
    
    if not user_data:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Update user data
    user = json.loads(user_data)
    
    # Update all fields that are not None
    for field, value in user_update.dict(exclude_unset=True).items():
        if value is not None:
            user[field] = value
    
    # Update timestamp
    user["updated_at"] = datetime.datetime.now(datetime.timezone.utc).isoformat()
    
    # Save back to Redis
    redis_client.set(f"user:{user_query.email}", json.dumps(user))
    
    # If email is updated, update the reference in Redis
    if user_update.email and user_update.email != user_query.email:
        redis_client.delete(f"user:{user_query.email}")
        redis_client.set(f"user:{user_update.email}", json.dumps(user))
        redis_client.srem("users", user_query.email)
        redis_client.sadd("users", user_update.email)
    
    return {"status": "success", "data": user}

@app.delete("/api/users/delete")
async def delete_user(user_query: UserQuery):
    # Check if user exists
    if not redis_client.exists(f"user:{user_query.email}"):
        raise HTTPException(status_code=404, detail="User not found")
    
    # Delete user from Redis
    redis_client.delete(f"user:{user_query.email}")
    redis_client.srem("users", user_query.email)
    
    return {"status": "success", "message": f"User {user_query.email} deleted successfully"}

@app.post("/api/users/bulk-create")
async def add_multiple_users(bulk_data: UserBulkCreate, background_tasks: BackgroundTasks):
    # Process users in background to handle many requests
    background_tasks.add_task(process_bulk_users, bulk_data.data)
    
    return {"status": "success", "message": f"Processing {len(bulk_data.data)} users in background"}

async def process_bulk_users(users_data):
    for user_data in users_data:
        # Skip if user already exists
        if redis_client.exists(f"user:{user_data.email}"):
            continue
        
        # Create user record
        user_dict = user_data.dict(exclude_unset=True)
        new_user = create_user_record(user_dict)
        
        # Store in Redis
        redis_client.set(f"user:{user_data.email}", json.dumps(new_user))
        redis_client.sadd("users", user_data.email)
        
        # Small delay to avoid overwhelming Redis
        await asyncio.sleep(0.01)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app", 
        host=os.getenv("HOST", "0.0.0.0"), 
        port=int(os.getenv("PORT", 8000)),
        reload=True
    )
