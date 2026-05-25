import hmac
import hashlib
import urllib.parse
import json
from fastapi import HTTPException

def verify_telegram_data(bot_token: str, init_data: str) -> dict:
    if not init_data:
        raise HTTPException(status_code=401, detail="X-Init-Data mungon")
    
    try:
        parsed_data = dict(urllib.parse.parse_qsl(init_data))
        if "hash" not in parsed_data:
            raise HTTPException(status_code=401, detail="Hash mungon")
        
        tg_hash = parsed_data.pop("hash")
        data_check_string = "\n".join(f"{k}={v}" for k, v in sorted(parsed_data.items()))
        
        secret_key = hmac.new(b"WebAppData", bot_token.encode(), hashlib.sha256).digest()
        calculated_hash = hmac.new(secret_key, data_check_string.encode(), hashlib.sha256).hexdigest()
        
        if calculated_hash != tg_hash:
            raise HTTPException(status_code=401, detail="Te dhena te paautorizuara!")
            
        return json.loads(parsed_data.get("user", "{}"))
    except Exception:
        raise HTTPException(status_code=401, detail="Format i gabuar i InitData")
