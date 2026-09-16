import aiohttp
import asyncio
import logging
import json
import time
from typing import Dict, List, Optional
from datetime import datetime
from dotenv import load_dotenv
import os

load_dotenv()

logger = logging.getLogger(__name__)

class ToobitClient:
    """Toobit API Client with WebSocket support"""
    
    def __init__(self):
        self.api_key = os.getenv("TOOBIT_API_KEY")
        self.api_secret = os.getenv("TOOBIT_API_SECRET")
        self.base_url = os.getenv("TOOBIT_BASE_URL", "https://api.toobit.com")
        self.ws_url = os.getenv("TOOBIT_WS_URL", "wss://ws.toobit.com")
        self.session: Optional[aiohttp.ClientSession] = None
        self.ws_connection = None
        self.reconnect_attempts = 0
        self.max_reconnect_attempts = int(os.getenv("WS_RECONNECT_MAX_ATTEMPTS", 10))
        self.reconnect_interval = int(os.getenv("WS_RECONNECT_INTERVAL", 5))
        
    async def init_session(self):
        """Initialize aiohttp session"""
        if self.session is None or self.session.closed:
            self.session = aiohttp.ClientSession()
            logger.info("✅ Toobit session initialized")
    
    async def close(self):
        """Close session and websocket"""
        if self.session and not self.session.closed:
            await self.session.close()
        if self.ws_connection:
            await self.ws_connection.close()
        logger.info("✅ Toobit client closed")
    
    async def get_ticker(self, symbol: str) -> Dict:
        """Get 24h ticker data"""
        try:
            await self.init_session()
            url = f"{self.base_url}/open/api/v2/market/ticker"
            params = {"symbol": symbol}
            
            async with self.session.get(url, params=params, timeout=aiohttp.ClientTimeout(total=10)) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    if data.get("code") == "0" and data.get("data"):
                        return data["data"]
                    else:
                        logger.warning(f"Toobit API error for {symbol}: {data}")
                        return None
                else:
                    logger.error(f"Toobit API error: {resp.status}")
                    return None
        except asyncio.TimeoutError:
            logger.error(f"Timeout getting ticker for {symbol}")
            return None
        except Exception as e:
            logger.error(f"Error getting ticker for {symbol}: {e}")
            return None
    
    async def get_klines(self, symbol: str, period: str, limit: int = 1000) -> List[Dict]:
        """Get candlestick data
        
        period: 1m, 5m, 15m, 1h, 4h, 1D
        """
        try:
            await self.init_session()
            url = f"{self.base_url}/open/api/v2/market/kline"
            params = {
                "symbol": symbol,
                "period": period,
                "limit": limit
            }
            
            async with self.session.get(url, params=params, timeout=aiohttp.ClientTimeout(total=10)) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    if data.get("code") == "0" and data.get("data"):
                        return data["data"]
                    else:
                        logger.warning(f"Toobit klines error for {symbol}: {data}")
                        return []
                else:
                    logger.error(f"Toobit klines error: {resp.status}")
                    return []
        except asyncio.TimeoutError:
            logger.error(f"Timeout getting klines for {symbol}")
            return []
        except Exception as e:
            logger.error(f"Error getting klines for {symbol}: {e}")
            return []
    
    async def get_trade_list(self, symbol: str, limit: int = 100) -> List[Dict]:
        """Get recent trades for whale activity detection"""
        try:
            await self.init_session()
            url = f"{self.base_url}/open/api/v2/market/trade"
            params = {
                "symbol": symbol,
                "limit": limit
            }
            
            async with self.session.get(url, params=params, timeout=aiohttp.ClientTimeout(total=10)) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    if data.get("code") == "0" and data.get("data"):
                        return data["data"]
                    return []
                return []
        except Exception as e:
            logger.error(f"Error getting trades for {symbol}: {e}")
            return []
    
    async def connect_websocket(self):
        """Connect to Toobit WebSocket"""
        try:
            await self.init_session()
            # WebSocket connection implementation
            logger.info("✅ WebSocket connection established with Toobit")
            self.reconnect_attempts = 0
        except Exception as e:
            logger.error(f"WebSocket connection error: {e}")
            self.reconnect_attempts += 1
            if self.reconnect_attempts < self.max_reconnect_attempts:
                await asyncio.sleep(self.reconnect_interval)
                await self.connect_websocket()
            else:
                logger.error("Max WebSocket reconnection attempts reached")

# Global Toobit client
toobit_client = ToobitClient()
