# 🧱 WALL - Premium Crypto Trading Telegram Mini App

A professional-grade cryptocurrency trading terminal built as a Telegram Mini App with real-time market data, advanced technical analysis, and automated signal generation.

## 🌟 Features

### Live Market Data
- Real-time price feeds from Toobit (BTCUSDT, ETHUSDT, SOLUSDT, XRPUSDT, DOGEUSDT, BNBUSDT, ADAUSDT, AVAXUSDT, LINKUSDT, SUIUSDT)
- 24h high/low, volume, and price movements
- WebSocket connection with automatic reconnection
- Fallback handling for API failures

### Whale Activity Monitor
- Real-time market flow visualization
- Large volume activity detection
- Market pressure indicators
- Based on legitimate order flow and volume data from Toobit

### Professional Charts
- Interactive candlestick charts (Lightweight Charts)
- Multiple timeframes: 1m, 5m, 15m, 1h, 4h, 1D
- Technical indicators: EMA20, EMA50, EMA200, RSI, MACD, Volume
- Live updates with market data

### Signal Center
- Premium signal generation based on multi-factor analysis
- Each signal includes: Entry, Stop Loss, Take Profit levels, Risk/Reward ratio
- Estimated profit percentages (not guaranteed)
- Signal strength visualization
- Detailed analysis reasoning

### Advanced Signal Engine
- **Trend Analysis**: EMA20, EMA50, EMA200
- **Momentum**: RSI14, MACD
- **Market Structure**: Support, Resistance, Breakout/Breakdown patterns
- **Volume Analysis**: Volume spike and confirmation
- **Volatility Management**: ATR-based dynamic stops and targets
- **Consensus Engine**: Quality signals with multi-condition validation
- **Late Entry Filter**: Rejects signals when price is too far from entry (> ATR)

### Entry Watcher
- Monitors live prices for entry point achievement
- One-time alerts when entry zone is reached
- No repeated alerts for the same signal
- Real-time Toobit price monitoring

### Telegram Integration
- Native Telegram Mini App support
- Telegram WebApp SDK integration
- Bot notifications for new signals
- Channel signal broadcasting
- User identity validation

### Premium UI
- Dark modern design with glass-morphism cards
- Persian font (Vazirmatn) for Persian text
- Inter font for English/numbers
- Mobile-first responsive layout
- RTL Persian interface
- LTR crypto data
- Smooth animations and transitions
- Professional skeleton loading
- Toast notifications

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- Node.js 18+
- SQLite3
- Telegram Bot Token
- Telegram Channel ID
- Toobit API credentials

### Local Development

#### Backend Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
nano .env  # Configure your settings
python -m uvicorn app.main:app --reload
```

#### Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

## 🌐 Production Deployment

See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed Linux/cPanel deployment instructions.

## 🔐 Security

- All secrets stored in `.env` files
- Never commit API keys or tokens
- Server-side Telegram initData validation
- HTTPS required for Telegram Mini Apps

## 📊 Project Structure

```
wall-trading-app/
├── frontend/              # React + TypeScript + Vite
├── backend/               # Python + FastAPI
├── data/                  # SQLite database
├── logs/                  # Application logs
├── .env.example           # Environment template
├── .gitignore
└── README.md
```

## 📄 License

Private - All rights reserved
