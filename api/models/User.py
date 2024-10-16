import uuid
from typing import Optional
from pydantic import BaseModel, Field, EmailStr
from datetime import datetime

from config.db import db

users = db['users']

class User(BaseModel):
  name: str = Field(..., title="Name", min_length=1)
  email: EmailStr = Field(..., title="Email")
  password: str = Field(..., title="Password", min_length=8)
  language: Optional[str] = Field(default="english", description="User's language preference")
  profile_pic: Optional[str] = Field(default="", description="URL to the user's profile picture")
  created_at: Optional[datetime] = Field(default=datetime.now())
  # updated_at: Optional[datetime] = None

  class Config:
    orm_mode = True