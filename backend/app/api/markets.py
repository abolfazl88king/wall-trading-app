from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc
from app.database import get_db
from app.models import MarketData
from app.schemas import MarketDataResponse
from app.services.market_data import market_data_service

router = APIRouter()

@router.get("/", response_model=list[MarketDataResponse])
async def get_all_markets():
    """Get all monitored market data"""
    markets = await market_data_service.get_all_market_data()
    return markets

@router.get("/{symbol}", response_model=MarketDataResponse)
async def get_market(symbol: str):
    """Get market data for specific symbol"""
    data = await market_data_service.get_market_data(symbol)
    if not data:
        return {"symbol": symbol, "price": 0, "high_24h": 0, "low_24h": 0, "volume_24h": 0, "change_24h_percent": 0}
    return data

@router.get("/top-movers/summary")
async def get_top_movers():
    """Get top gainers and losers"""
    return await market_data_service.get_top_movers(5)
