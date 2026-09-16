from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from enum import Enum

class SignalDirection(str, Enum):
    LONG = "LONG"
    SHORT = "SHORT"

class TimeFrame(str, Enum):
    ONE_MINUTE = "1m"
    FIVE_MINUTES = "5m"
    FIFTEEN_MINUTES = "15m"
    ONE_HOUR = "1h"
    FOUR_HOURS = "4h"
    ONE_DAY = "1D"

# Market Data Schemas
class MarketDataBase(BaseModel):
    symbol: str
    price: float
    high_24h: float
    low_24h: float
    volume_24h: float
    change_24h_percent: float
    market_cap: Optional[float] = None

class MarketDataResponse(MarketDataBase):
    id: int
    last_updated: datetime
    
    class Config:
        from_attributes = True

# Candle Schemas
class CandleBase(BaseModel):
    symbol: str
    timeframe: TimeFrame
    open_price: float
    high: float
    low: float
    close_price: float
    volume: float
    timestamp: datetime

class CandleResponse(CandleBase):
    id: int
    
    class Config:
        from_attributes = True

# Signal Schemas
class SignalBase(BaseModel):
    symbol: str
    direction: SignalDirection
    entry_price: float
    entry_range_min: float
    entry_range_max: float
    stop_loss: float
    take_profit_1: float
    take_profit_2: float
    risk_reward_ratio: float
    confidence: float
    trend_score: float
    momentum_score: float
    structure_score: float
    volume_score: float
    volatility_score: float
    reasons: List[str]
    atr_value: float
    late_entry_rejected: bool = False

class SignalCreate(SignalBase):
    pass

class SignalResponse(SignalBase):
    id: int
    is_active: bool
    entry_alert_sent: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class SignalDetailResponse(SignalResponse):
    current_price: Optional[float] = None
    time_until_expiry: Optional[int] = None  # seconds

# User Schemas
class UserBase(BaseModel):
    telegram_id: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    username: Optional[str] = None
    language_code: str = "en"

class UserCreate(UserBase):
    pass

class UserUpdate(BaseModel):
    notifications_enabled: Optional[bool] = None
    language_code: Optional[str] = None

class UserResponse(UserBase):
    id: int
    is_premium: bool
    notifications_enabled: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

# Entry Alert Schemas
class EntryAlertResponse(BaseModel):
    id: int
    signal_id: int
    symbol: str
    entry_price: float
    current_price: float
    alert_sent: bool
    alert_sent_at: Optional[datetime]
    created_at: datetime
    
    class Config:
        from_attributes = True

# Whale Activity Schemas
class WhaleActivityResponse(BaseModel):
    id: int
    symbol: str
    activity_type: str  # BUY, SELL, LARGE_VOLUME
    volume: float
    price: float
    volume_percent: float
    market_impact: float
    timestamp: datetime
    
    class Config:
        from_attributes = True

# Telegram Auth Schemas
class TelegramWebAppData(BaseModel):
    init_data: str

class TelegramUser(BaseModel):
    id: int
    is_bot: bool
    first_name: str
    last_name: Optional[str] = None
    username: Optional[str] = None
    language_code: Optional[str] = None
    is_premium: Optional[bool] = False
