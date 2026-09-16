# WALL Backend - Deployment Guide for cPanel

## Environment Setup

```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

## Configure .env

Edit `backend/.env` with your credentials:
- TOOBIT_API_KEY
- TOOBIT_API_SECRET
- TELEGRAM_BOT_TOKEN
- TELEGRAM_CHANNEL_ID
- CORS_ORIGINS
- DATABASE_URL

## Run Locally

```bash
source venv/bin/activate
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## cPanel Deployment

### Option 1: Using cPanel Python App

1. Go to cPanel > Setup Python App
2. Create Application:
   - Python version: 3.10+
   - App directory: /home/user/public_html/wall/backend
   - App startup file: wsgi.py
   - Application URL: /api
3. Install dependencies through cPanel
4. Restart application

### Option 2: Manual Setup with Systemd

1. Create systemd service file:
```bash
sudo nano /etc/systemd/system/wall-backend.service
```

2. Add:
```ini
[Unit]
Description=WALL Trading Backend
After=network.target

[Service]
Type=notify
User=yourusername
WorkingDirectory=/home/user/public_html/wall/backend
Environment="PATH=/home/user/public_html/wall/backend/venv/bin"
ExecStart=/home/user/public_html/wall/backend/venv/bin/gunicorn -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000 app.main:app
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

3. Enable and start:
```bash
sudo systemctl daemon-reload
sudo systemctl enable wall-backend
sudo systemctl start wall-backend
```

## Database

Database is stored in `data/wall.db` automatically created on first run.

## Troubleshooting

- Check logs: `journalctl -u wall-backend -f`
- Restart: `sudo systemctl restart wall-backend`
- Check status: `sudo systemctl status wall-backend`
