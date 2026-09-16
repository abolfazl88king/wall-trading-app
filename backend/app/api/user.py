from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.models import User
from app.schemas import UserResponse, UserCreate, UserUpdate
from sqlalchemy import select

router = APIRouter()

@router.post("/register", response_model=UserResponse)
async def register_user(user: UserCreate, db: AsyncSession = Depends(get_db)):
    stmt = select(User).where(User.telegram_id == user.telegram_id)
    existing = await db.execute(stmt)
    if existing.scalars().first():
        raise HTTPException(status_code=400, detail="User already registered")
    
    db_user = User(**user.dict())
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user

@router.get("/profile", response_model=UserResponse)
async def get_profile(telegram_id: str, db: AsyncSession = Depends(get_db)):
    stmt = select(User).where(User.telegram_id == telegram_id)
    user = await db.execute(stmt)
    user_obj = user.scalars().first()
    if not user_obj:
        raise HTTPException(status_code=404, detail="User not found")
    return user_obj

@router.put("/profile/{telegram_id}", response_model=UserResponse)
async def update_profile(telegram_id: str, user: UserUpdate, db: AsyncSession = Depends(get_db)):
    stmt = select(User).where(User.telegram_id == telegram_id)
    db_user = await db.execute(stmt)
    user_obj = db_user.scalars().first()
    if not user_obj:
        raise HTTPException(status_code=404, detail="User not found")
    
    update_data = user.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(user_obj, key, value)
    
    db.add(user_obj)
    await db.commit()
    await db.refresh(user_obj)
    return user_obj
