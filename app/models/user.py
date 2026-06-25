from typing import ClassVar, Optional
from sqlmodel import SQLModel, Field

class User(SQLModel, table=True):
    __tablename__ = "users"  # type: ignore
    
    id: str = Field(primary_key=True)
    name: str
    email: Optional[str] = None
