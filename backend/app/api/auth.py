from fastapi import APIRouter, HTTPException
import json
import hmac
import hashlib
import os
from app.schemas import TelegramWebAppData
from dotenv import load_dotenv

load_dotenv()

router = APIRouter()

@router.post("/validate-mini-app")
async def validate_mini_app(data: TelegramWebAppData):
    """Validate Telegram Mini App initData"""
    try:
        bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
        if not bot_token:
            raise HTTPException(status_code=500, detail="Bot token not configured")
        
        init_data = data.init_data
        
        # Parse init data
        init_data_dict = dict(x.split('=') for x in init_data.split('&'))
        signature = init_data_dict.pop('hash')
        
        # Verify signature
        check_string = '\n'.join(
            f'{k}={v}' for k, v in sorted(init_data_dict.items())
        )
        secret_key = hmac.new(
            b'WebAppData',
            bot_token.encode(),
            hashlib.sha256
        ).digest()
        computed_hash = hmac.new(
            secret_key,
            check_string.encode(),
            hashlib.sha256
        ).hexdigest()
        
        if computed_hash != signature:
            raise HTTPException(status_code=401, detail="Invalid signature")
        
        user_data = json.loads(init_data_dict.get('user', '{}'))
        return {
            "valid": True,
            "user": user_data
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
