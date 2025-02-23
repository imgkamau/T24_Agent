from pydantic import BaseModel, Field, validator
from typing import List, Dict

class Message(BaseModel):
    role: str = Field(..., pattern="^(user|system|assistant)$")
    content: str = Field(..., min_length=1, max_length=4096)
    
    @validator('content')
    def validate_content(cls, v):
        if not v.strip():
            raise ValueError('Content cannot be empty or whitespace')
        return v.strip()

class Conversation(BaseModel):
    user_id: str = Field(..., min_length=3)
    messages: List[Message]
    metadata: Dict = {} 