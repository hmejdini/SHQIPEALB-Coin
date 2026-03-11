from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import random

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Te dhenat e burses
market = {"price": 5.00, "trend": "stable"}

@app.get("/market")
async def get_market():
    change = random.uniform(-0.03, 0.03)
    market["price"] += change
    market["trend"] = "up" if change > 0 else "down"
    return market

@app.get("/buy/{amount}")
async def buy(amount: int):
    market["price"] += (amount * 0.02)
    return {"status": "success", "price": market["price"]}
