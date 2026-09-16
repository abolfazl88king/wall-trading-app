from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc
from app.database import get_db
from app.models import Signal
from app.schemas import SignalResponse, SignalDetailResponse

router = APIRouter()

@router.get("/", response_model=list[SignalResponse])
async def get_signals(limit: int = 50, db: AsyncSession = Depends(get_db)):
    """Get latest signals"""
    stmt = select(Signal).where(Signal.is_active == True).order_by(desc(Signal.created_at)).limit(limit)
    result = await db.execute(stmt)
    return result.scalars().all()

@router.get("/{signal_id}", response_model=SignalDetailResponse)
async def get_signal(signal_id: int, db: AsyncSession = Depends(get_db)):
    """Get signal details"""
    stmt = select(Signal).where(Signal.id == signal_id)
    result = await db.execute(stmt)
    signal = result.scalars().first()
    if not signal:
        return {"detail": "Signal not found"}
    return signal

@router.get("/by-symbol/{symbol}", response_model=list[SignalResponse])
async def get_signals_by_symbol(symbol: str, db: AsyncSession = Depends(get_db)):
    """Get signals for specific symbol"""
    stmt = select(Signal).where(
        (Signal.symbol == symbol) & 
        (Signal.is_active == True)
    ).order_by(desc(Signal.created_at))
    result = await db.execute(stmt)
    return result.scalars().all()
