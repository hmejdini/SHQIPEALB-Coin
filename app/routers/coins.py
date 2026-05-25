import time
from fastapi import APIRouter, Depends, Header, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.core.database import get_db
from app.core.security import verify_telegram_data
from app.models.user import User
from app.core.config import settings

router = APIRouter(prefix="/api", tags=["Coins"])

@router.post("/claim")
async def claim_coins(x_init_data: str = Header(..., alias="X-Init-Data"), db: AsyncSession = Depends(get_db)):
    # 1. Verifikimi i të dhënave nga Telegrami
    tg_user = verify_telegram_data(settings.BOT_TOKEN, x_init_data)
    tg_id = tg_user.get("id")
    
    if not tg_id:
        raise HTTPException(status_code=400, detail="Telegram ID nuk u gjet")

    # 2. Kontrolli në databazë nëse ekziston përdoruesi
    result = await db.execute(select(User).where(User.telegram_id == tg_id))
    user = result.scalar_one_or_none()
    
    current_time = time.time()

    # 3. Nëse është përdorues i ri, regjistroje dhe jepi 10 AlbCoins e para
    if not user:
        user = User(
            telegram_id=tg_id,
            username=tg_user.get("username"),
            first_name=tg_user.get("first_name"),
            balance=10,
            last_claim_time=current_time
        )
        db.add(user)
        await db.commit()
        return {"success": True, "balance": user.balance}

    # 4. Kontrolli i kohës prej 10 sekondash (Cooldown)
    if current_time - user.last_claim_time < 10:
        time_left = int(10 - (current_time - user.last_claim_time))
        raise HTTPException(status_code=429, detail=f"Prisni edhe {time_left} sekonda.")

    # 5. Shtimi i monedhave në bilanc
    user.balance += 10
    user.last_claim_time = current_time
    await db.commit()
    await db.refresh(user)

    return {"success": True, "balance": user.balance}
