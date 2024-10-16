from pydantic import BaseModel, Field
from typing import List, Optional
from bson import ObjectId
from datetime import datetime
from config.db import db

messages = db['messages']
conversations = db['conversations']

class PyObjectId(ObjectId):
    """Custom Pydantic-compatible ObjectId"""
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError('Invalid objectid')
        return ObjectId(v)

class Message(BaseModel):
    text: Optional[str] = Field(default="")
    imageUrl: Optional[str] = Field(default="")
    videoUrl: Optional[str] = Field(default="")
    audioUrl: Optional[str] = Field(default="")
    seen: Optional[bool] = Field(default=False)
    msgByUserId: PyObjectId = Field(..., alias="msgByUserId")
    sent_at: Optional[datetime] = Field(default_factory=datetime.now)

    class Config:
        orm_mode = True
        json_encoders = {ObjectId: str}
        allow_population_by_field_name = True

# Conversation Schema
class Conversation(BaseModel):
    sender: PyObjectId = Field(..., alias="sender")
    receiver: PyObjectId = Field(..., alias="receiver")
    messages: Optional[List[PyObjectId]] = Field(default=[])

    class Config:
        orm_mode = True
        json_encoders = {ObjectId: str}
        allow_population_by_field_name = True