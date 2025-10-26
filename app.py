# app.py
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from uuid import uuid4, UUID
from datetime import datetime
from threading import Lock

app = FastAPI(title="User Management API (Basic)")


class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=32)
    email: EmailStr
    display_name: Optional[str] = None


class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    display_name: Optional[str] = None


class UserOut(BaseModel):
    id: UUID
    username: str
    email: EmailStr
    display_name: Optional[str] = None
    created_at: datetime


# In-memory store
_store = {}
_store_lock = Lock()


@app.post("/api/v1/users", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def create_user(payload: UserCreate):
    with _store_lock:
        # simple uniqueness check on username/email
        if any(u["username"] == payload.username for u in _store.values()):
            raise HTTPException(status_code=400, detail="username_already_exists")
        if any(u["email"] == payload.email for u in _store.values()):
            raise HTTPException(status_code=400, detail="email_already_exists")

        user_id = uuid4()
        now = datetime.utcnow()
        user = {
            "id": user_id,
            "username": payload.username,
            "email": payload.email,
            "display_name": payload.display_name,
            "created_at": now,
        }
        _store[str(user_id)] = user
        return user


@app.get("/api/v1/users/{user_id}", response_model=UserOut)
def get_user(user_id: UUID):
    u = _store.get(str(user_id))
    if not u:
        raise HTTPException(status_code=404, detail="user_not_found")
    return u


@app.get("/api/v1/users", response_model=List[UserOut])
def list_users(limit: int = 50):
    # simple list; in production return paginated cursor
    items = list(_store.values())[:limit]
    return items


@app.patch("/api/v1/users/{user_id}", response_model=UserOut)
def update_user(user_id: UUID, payload: UserUpdate):
    key = str(user_id)
    with _store_lock:
        u = _store.get(key)
        if not u:
            raise HTTPException(status_code=404, detail="user_not_found")
        if payload.email:
            # check email uniqueness
            if any(
                other["email"] == payload.email and other["id"] != user_id
                for other in _store.values()
            ):
                raise HTTPException(status_code=400, detail="email_already_exists")
            u["email"] = payload.email
        if payload.display_name is not None:
            u["display_name"] = payload.display_name
        _store[key] = u
        return u


@app.delete("/api/v1/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: UUID):
    key = str(user_id)
    with _store_lock:
        if key not in _store:
            raise HTTPException(status_code=404, detail="user_not_found")
        del _store[key]
    return None


@app.post("/api/v1/users/{user_id}/password", status_code=status.HTTP_201_CREATED)
def create_password(user_id: UUID, payload: dict):
    key = str(user_id)
    print(user_id)
    print("cheese")
    with _store_lock:
        u = _store.get(key)
        if not u:
            raise HTTPException(status_code=404, detail="user_not_found")
        # In a real application, you would hash the password and store it securely
        u["password"] = payload.get("password")
        _store[key] = u
    return None
