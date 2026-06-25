from sqlmodel import SQLModel, Field

class UserInterest(SQLModel, table=True):
    __tablename__ = "user_interests"  # type: ignore
    
    user_id: str = Field(primary_key=True)
    interest: str = Field(primary_key=True)
