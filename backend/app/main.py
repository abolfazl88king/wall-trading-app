from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
import logging
from pathlib import Path
import os
from dotenv import load_dotenv

from app.api import markets, signals, charts, user, auth
from app.services.market_data import MarketDataService
from app.services.signal_engine import SignalEngine
from app.services.entry_watcher import EntryWatcher
from app.database import init_db

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Global services
market_service = None
signal_engine = None
entry_watcher = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info("Starting WALL Trading Backend...")
    await init_db()
    
    global market_service, signal_engine, entry_watcher
    market_service = MarketDataService()
    signal_engine = SignalEngine(market_service)
    entry_watcher = EntryWatcher(market_service)
    
    await market_service.start()
    await signal_engine.start()
    await entry_watcher.start()
    
    logger.info("✅ WALL Backend started successfully")
    yield
    
    # Shutdown
    logger.info("Shutting down WALL Backend...")
    await market_service.stop()
    await signal_engine.stop()
    await entry_watcher.stop()
    logger.info("✅ WALL Backend stopped")

app = FastAPI(
    title=os.getenv("API_TITLE", "WALL Trading Terminal"),
    version=os.getenv("API_VERSION", "1.0.0"),
    description="Premium Crypto Trading Telegram Mini App",
    lifespan=lifespan
)

# CORS Configuration
cors_origins = os.getenv("CORS_ORIGINS", "[\"http://localhost:5173\"]")
import json
try:
    cors_origins = json.loads(cors_origins)
except:
    cors_origins = ["http://localhost:5173", "http://localhost:3000"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
app.include_router(user.router, prefix="/api/user", tags=["user"])
app.include_router(markets.router, prefix="/api/markets", tags=["markets"])
app.include_router(signals.router, prefix="/api/signals", tags=["signals"])
app.include_router(charts.router, prefix="/api/charts", tags=["charts"])

@app.get("/")
async def root():
    return {
        "name": "WALL Trading Terminal",
        "version": "1.0.0",
        "status": "online",
        "endpoints": {
            "markets": "/api/markets",
            "signals": "/api/signals",
            "charts": "/api/charts",
            "user": "/api/user",
            "auth": "/api/auth",
            "ws_markets": "/ws/markets",
            "health": "/health"
        }
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "WALL Backend"}

class ConnectionManager:
    def __init__(self):
        self.active_connections: dict = {}

    async def connect(self, websocket: WebSocket, client_id: str):
        await websocket.accept()
        self.active_connections[client_id] = websocket
        logger.info(f"Client {client_id} connected")

    def disconnect(self, client_id: str):
        if client_id in self.active_connections:
            del self.active_connections[client_id]
            logger.info(f"Client {client_id} disconnected")

    async def broadcast(self, message: dict):
        disconnected = []
        for client_id, connection in self.active_connections.items():
            try:
                await connection.send_json(message)
            except Exception as e:
                logger.error(f"Error sending to {client_id}: {e}")
                disconnected.append(client_id)
        
        for client_id in disconnected:
            self.disconnect(client_id)

manager = ConnectionManager()

@app.websocket("/ws/markets")
async def websocket_markets(websocket: WebSocket):
    client_id = f"{websocket.client[0]}:{websocket.client[1]}"
    await manager.connect(websocket, client_id)
    try:
        while True:
            data = await websocket.receive_text()
            # Echo back for keep-alive
            await websocket.send_text(data)
    except WebSocketDisconnect:
        manager.disconnect(client_id)
    except Exception as e:
        logger.error(f"WebSocket error for {client_id}: {e}")
        manager.disconnect(client_id)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=os.getenv("API_HOST", "0.0.0.0"),
        port=int(os.getenv("API_PORT", 8000)),
        reload=os.getenv("DEBUG", "False") == "True"
    )
