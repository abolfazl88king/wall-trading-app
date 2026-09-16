import asyncio
import logging
from typing import Dict, List, Optional
from datetime import datetime, timedelta
import numpy as np
from app.services.toobit_client import toobit_client

logger = logging.getLogger(__name__)

class MarketDataService:
    """Service for fetching and managing market data from Toobit"""
    
    def __init__(self):
        self.monitored_symbols = [
            "BTCUSDT", "ETHUSDT", "SOLUSDT", "XRPUSDT", 
            "DOGEUSDT", "BNBUSDT", "ADAUSDT", "AVAXUSDT", 
            "LINKUSDT", "SUIUSDT"
        ]
        self.market_data: Dict[str, Dict] = {}
        self.is_running = False
        self.update_interval = 5  # seconds
        self.cache_ttl = 60  # seconds
        self.last_update = {}
    
    async def start(self):
        """Start market data service"""
        self.is_running = True
        logger.info("🚀 MarketDataService started")
        asyncio.create_task(self._update_loop())
    
    async def stop(self):
        """Stop market data service"""
        self.is_running = False
        logger.info("⛔ MarketDataService stopped")
    
    async def _update_loop(self):
        """Continuously update market data"""
        while self.is_running:
            try:
                tasks = [self.update_ticker(symbol) for symbol in self.monitored_symbols]
                await asyncio.gather(*tasks, return_exceptions=True)
                await asyncio.sleep(self.update_interval)
            except Exception as e:
                logger.error(f"Error in market data update loop: {e}")
                await asyncio.sleep(self.update_interval)
    
    async def update_ticker(self, symbol: str):
        """Update ticker data for a symbol"""
        try:
            ticker = await toobit_client.get_ticker(symbol)
            if ticker:
                self.market_data[symbol] = {
                    "symbol": symbol,
                    "price": float(ticker.get("last", 0)),
                    "high_24h": float(ticker.get("high24h", 0)),
                    "low_24h": float(ticker.get("low24h", 0)),
                    "volume_24h": float(ticker.get("volume", 0)),
                    "change_24h_percent": float(ticker.get("change", 0)),
                    "timestamp": datetime.utcnow().isoformat()
                }
                self.last_update[symbol] = datetime.utcnow()
                logger.debug(f"Updated {symbol}: ${self.market_data[symbol]['price']}")
        except Exception as e:
            logger.error(f"Error updating ticker for {symbol}: {e}")
    
    async def get_market_data(self, symbol: str) -> Optional[Dict]:
        """Get latest market data for a symbol"""
        if symbol not in self.market_data:
            await self.update_ticker(symbol)
        
        data = self.market_data.get(symbol)
        if data:
            # Check if data is stale
            last_update = self.last_update.get(symbol)
            if last_update and (datetime.utcnow() - last_update).seconds > self.cache_ttl:
                await self.update_ticker(symbol)
                data = self.market_data.get(symbol)
        
        return data
    
    async def get_all_market_data(self) -> List[Dict]:
        """Get market data for all monitored symbols"""
        return [data for data in self.market_data.values() if data]
    
    async def get_top_movers(self, limit: int = 5) -> List[Dict]:
        """Get top gainers and losers"""
        try:
            all_data = await self.get_all_market_data()
            
            # Sort by change percentage
            sorted_data = sorted(
                all_data,
                key=lambda x: float(x.get("change_24h_percent", 0)),
                reverse=True
            )
            
            gainers = sorted_data[:limit]
            losers = sorted_data[-limit:]
            
            return {"gainers": gainers, "losers": losers}
        except Exception as e:
            logger.error(f"Error getting top movers: {e}")
            return {"gainers": [], "losers": []}
    
    async def get_candles(self, symbol: str, timeframe: str, limit: int = 100) -> List[Dict]:
        """Get candlestick data"""
        try:
            candles = await toobit_client.get_klines(symbol, timeframe, limit)
            return candles
        except Exception as e:
            logger.error(f"Error getting candles for {symbol}: {e}")
            return []
    
    async def calculate_indicators(self, candles: List[Dict]) -> Dict:
        """Calculate technical indicators from candles"""
        try:
            if len(candles) < 20:
                return {}
            
            # Extract close prices
            closes = np.array([float(c["c"]) for c in candles])
            
            # EMA calculations
            ema_20 = self._calculate_ema(closes, 20)
            ema_50 = self._calculate_ema(closes, 50)
            ema_200 = self._calculate_ema(closes, 200)
            
            # RSI calculation
            rsi = self._calculate_rsi(closes, 14)
            
            # ATR calculation
            highs = np.array([float(c["h"]) for c in candles])
            lows = np.array([float(c["l"]) for c in candles])
            atr = self._calculate_atr(highs, lows, closes, 14)
            
            # MACD calculation
            macd_line, signal_line, histogram = self._calculate_macd(closes)
            
            return {
                "ema_20": float(ema_20[-1]) if len(ema_20) > 0 else None,
                "ema_50": float(ema_50[-1]) if len(ema_50) > 0 else None,
                "ema_200": float(ema_200[-1]) if len(ema_200) > 0 else None,
                "rsi": float(rsi[-1]) if len(rsi) > 0 else None,
                "atr": float(atr[-1]) if len(atr) > 0 else None,
                "macd": float(macd_line[-1]) if len(macd_line) > 0 else None,
                "macd_signal": float(signal_line[-1]) if len(signal_line) > 0 else None,
                "macd_histogram": float(histogram[-1]) if len(histogram) > 0 else None,
            }
        except Exception as e:
            logger.error(f"Error calculating indicators: {e}")
            return {}
    
    @staticmethod
    def _calculate_ema(prices: np.ndarray, period: int) -> np.ndarray:
        """Calculate Exponential Moving Average"""
        return np.array(prices).ewm(span=period, adjust=False).mean()
    
    @staticmethod
    def _calculate_rsi(prices: np.ndarray, period: int = 14) -> np.ndarray:
        """Calculate Relative Strength Index"""
        prices = np.array(prices)
        deltas = np.diff(prices)
        seed = deltas[:period+1]
        up = seed[seed >= 0].sum() / period
        down = -seed[seed < 0].sum() / period
        rs = up / down if down != 0 else 0
        rsi = np.zeros_like(prices)
        rsi[:period] = 100.0 - 100.0 / (1.0 + rs)
        
        for i in range(period, len(prices)):
            delta = deltas[i-1]
            if delta > 0:
                upval = delta
                downval = 0.0
            else:
                upval = 0.0
                downval = -delta
            
            up = (up * (period - 1) + upval) / period
            down = (down * (period - 1) + downval) / period
            rs = up / down if down != 0 else 0
            rsi[i] = 100.0 - 100.0 / (1.0 + rs)
        
        return rsi
    
    @staticmethod
    def _calculate_atr(highs: np.ndarray, lows: np.ndarray, closes: np.ndarray, period: int = 14) -> np.ndarray:
        """Calculate Average True Range"""
        highs = np.array(highs)
        lows = np.array(lows)
        closes = np.array(closes)
        
        tr1 = highs - lows
        tr2 = np.abs(highs - np.roll(closes, 1))
        tr3 = np.abs(lows - np.roll(closes, 1))
        tr = np.maximum(tr1, np.maximum(tr2, tr3))
        atr = np.zeros_like(tr)
        atr[period-1] = tr[:period].mean()
        
        for i in range(period, len(tr)):
            atr[i] = (atr[i-1] * (period - 1) + tr[i]) / period
        
        return atr
    
    @staticmethod
    def _calculate_macd(prices: np.ndarray, fast: int = 12, slow: int = 26, signal: int = 9):
        """Calculate MACD"""
        prices = np.array(prices)
        ema_fast = prices.ewm(span=fast, adjust=False).mean()
        ema_slow = prices.ewm(span=slow, adjust=False).mean()
        macd_line = ema_fast - ema_slow
        signal_line = macd_line.ewm(span=signal, adjust=False).mean()
        histogram = macd_line - signal_line
        
        return macd_line, signal_line, histogram

# Global instance
market_data_service = MarketDataService()
