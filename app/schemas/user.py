from pydantic import BaseModel
from typing import List

class UserInterestCreate(BaseModel):
    user_id: str
    interests: List[str]

class UserInterestResponse(BaseModel):
    user_id: str
    interest: str

class UserInterestsListResponse(BaseModel):
    user_id: str
    interests: List[str]

class UserCreate(BaseModel):
    id: str
    name: str
    email: str | None = None

class UserResponse(BaseModel):
    id: str
    name: str
    email: str | None = None
