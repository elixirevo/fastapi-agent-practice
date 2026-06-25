from fastapi import APIRouter, HTTPException
from sqlmodel import select
from app.core.database import get_session
from app.models.user_interest import UserInterest
from app.models.user import User
from app.schemas.user import (
    UserInterestCreate,
    UserInterestsListResponse,
    UserInterestResponse,
    UserCreate,
    UserResponse
)

router = APIRouter()

@router.post("", response_model=UserResponse)
async def create_user(payload: UserCreate):
    """유저를 신규 생성하는 API입니다."""
    async with get_session() as session:
        statement = select(User).where(User.id == payload.id)
        result = await session.execute(statement)
        existing = result.scalar_one_or_none()
        
        if existing:
            raise HTTPException(status_code=400, detail="User with this ID already exists.")
        
        new_user = User(id=payload.id, name=payload.name, email=payload.email)
        session.add(new_user)
        await session.commit()
        await session.refresh(new_user)
        return new_user

@router.get("/{user_id}", response_model=UserResponse)
async def read_user(user_id: str):
    """특정 유저의 상세 정보를 조회하는 API입니다."""
    async with get_session() as session:
        statement = select(User).where(User.id == user_id)
        result = await session.execute(statement)
        user = result.scalar_one_or_none()
        
        if not user:
            raise HTTPException(status_code=404, detail="User not found.")
        return user

@router.post("/interests", response_model=UserInterestsListResponse)
async def create_user_interests(payload: UserInterestCreate):
    """유저의 관심사 목록을 일괄 등록하는 API입니다."""
    async with get_session() as session:
        # 이미 등록된 관심사 조회
        statement = select(UserInterest).where(UserInterest.user_id == payload.user_id)
        result = await session.execute(statement)
        existing_interests = {item.interest for item in result.scalars().all()}
        
        new_interests_saved = []
        for interest in payload.interests:
            if interest not in existing_interests:
                new_item = UserInterest(user_id=payload.user_id, interest=interest)
                session.add(new_item)
                new_interests_saved.append(interest)
        
        if new_interests_saved:
            await session.commit()
            
        updated_interests = list(existing_interests.union(new_interests_saved))
        return UserInterestsListResponse(user_id=payload.user_id, interests=updated_interests)

@router.get("/{user_id}/interests", response_model=UserInterestsListResponse)
async def read_user_interests(user_id: str):
    """특정 유저의 관심사 목록을 조회하는 API입니다."""
    async with get_session() as session:
        statement = select(UserInterest).where(UserInterest.user_id == user_id)
        result = await session.execute(statement)
        interests_objects = result.scalars().all()
        
        interests = [item.interest for item in interests_objects]
        return UserInterestsListResponse(user_id=user_id, interests=interests)
