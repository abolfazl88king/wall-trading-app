from fastapi import APIRouter
from app.services.market_data import market_data_service

router = APIRouter()

@router.get("/{symbol}/candles")
async def get_candles(symbol: str, timeframe: str = "1h", limit: int = 100):
    """Get candlestick data"""
    candles = await market_data_service.get_candles(symbol, timeframe, limit)
    return {"symbol": symbol, "timeframe": timeframe, "candles": candles}

@router.get("/{symbol}/indicators")
async def get_indicators(symbol: str, timeframe: str = "1h"):
    """Get technical indicators"""
    candles = await market_data_service.get_candles(symbol, timeframe, 200)
    if not candles:
        return {"symbol": symbol, "timeframe": timeframe, "indicators": {}}
    
    indicators = await market_data_service.calculate_indicators(candles)
    return {"symbol": symbol, "timeframe": timeframe, "indicators": indicators}
