from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, Text, JSON
from sqlalchemy.sql import func
from app.database import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    telegram_id = Column(String, unique=True, index=True)
    first_name = Column(String, nullable=True)
    last_name = Column(String, nullable=True)
    username = Column(String, nullable=True)
    language_code = Column(String, default="en")
    is_premium = Column(Boolean, default=False)
    notifications_enabled = Column(Boolean, default=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

class Signal(Base):
    __tablename__ = "signals"
    
    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String, index=True)  # e.g., BTCUSDT
    direction = Column(String)  # LONG or SHORT
    entry_price = Column(Float)
    entry_range_min = Column(Float)
    entry_range_max = Column(Float)
    stop_loss = Column(Float)
    take_profit_1 = Column(Float)
    take_profit_2 = Column(Float)
    risk_reward_ratio = Column(Float)
    confidence = Column(Float)  # 0.0 to 1.0
    
    # Analysis components
    trend_score = Column(Float, default=0.0)  # EMA analysis
    momentum_score = Column(Float, default=0.0)  # RSI + MACD
    structure_score = Column(Float, default=0.0)  # Support/Resistance
    volume_score = Column(Float, default=0.0)  # Volume analysis
    volatility_score = Column(Float, default=0.0)  # ATR analysis
    
    # Reasons and details
    reasons = Column(JSON)  # Array of analysis reasons
    atr_value = Column(Float)  # ATR value for late entry check
    late_entry_rejected = Column(Boolean, default=False)
    
    # Status
    is_active = Column(Boolean, default=True)
    entry_alert_sent = Column(Boolean, default=False)
    
    created_at = Column(DateTime, server_default=func.now(), index=True)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

class EntryAlert(Base):
    __tablename__ = "entry_alerts"
    
    id = Column(Integer, primary_key=True, index=True)
    signal_id = Column(Integer, index=True)
    symbol = Column(String, index=True)
    entry_price = Column(Float)
    current_price = Column(Float)
    alert_sent = Column(Boolean, default=False)
    alert_sent_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

class MarketData(Base):
    __tablename__ = "market_data"
    
    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String, index=True)
    price = Column(Float)
    high_24h = Column(Float)
    low_24h = Column(Float)
    volume_24h = Column(Float)
    change_24h_percent = Column(Float)
    market_cap = Column(Float, nullable=True)
    last_updated = Column(DateTime, server_default=func.now(), onupdate=func.now(), index=True)

class Candle(Base):
    __tablename__ = "candles"
    
    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String, index=True)
    timeframe = Column(String)  # 1m, 5m, 15m, 1h, 4h, 1D
    open_price = Column(Float)
    high = Column(Float)
    low = Column(Float)
    close_price = Column(Float)
    volume = Column(Float)
    timestamp = Column(DateTime, index=True)
    created_at = Column(DateTime, server_default=func.now())

class WhaleActivity(Base):
    __tablename__ = "whale_activity"
    
    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String, index=True)
    activity_type = Column(String)  # BUY, SELL, LARGE_VOLUME
    volume = Column(Float)
    price = Column(Float)
    volume_percent = Column(Float)  # Percentage of 24h volume
    market_impact = Column(Float)  # 0.0 to 1.0
    timestamp = Column(DateTime, server_default=func.now(), index=True)

class AlertState(Base):
    __tablename__ = "alert_states"
    
    id = Column(Integer, primary_key=True, index=True)
    signal_id = Column(Integer, unique=True, index=True)
    alert_type = Column(String)  # ENTRY, TP1, TP2, SL
    triggered = Column(Boolean, default=False)
    triggered_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, server_default=func.now())

class Settings(Base):
    __tablename__ = "settings"
    
    id = Column(Integer, primary_key=True, index=True)
    key = Column(String, unique=True, index=True)
    value = Column(Text)
    description = Column(String, nullable=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
