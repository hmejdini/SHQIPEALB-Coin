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

# Databaza në memorje
market = {
    "price": 0.50,
    "last_buy": 0
}

# Ruajmë të dhënat e përdoruesve: {"username": {"referrals": 0, "balance": 0}}
users_db = {}

@app.get("/market")
async def get_market():
    market["price"] += random.uniform(-0.005, 0.005)
    if market["price"] < 0.10: market["price"] = 0.10
    
    temp_buy = market["last_buy"]
    market["last_buy"] = 0
    return {"price": round(market["price"], 2), "last_buy": temp_buy}

@app.get("/buy/{username}/{amount}")
async def buy_coin(username: str, amount: int):
    market["price"] += (amount * 0.01)
    market["last_buy"] = amount
    
    if username not in users_db:
        users_db[username] = {"referrals": 0, "balance": 0}
    users_db[username]["balance"] += amount
    
    return {"status": "success", "new_price": round(market["price"], 2)}

@app.post("/referral/{username}")
async def add_referral(username: str):
    if username not in users_db:
        users_db[username] = {"referrals": 0, "balance": 0}
    
    users_db[username]["referrals"] += 1
    
    if users_db[username]["referrals"] >= 5:
        users_db[username]["referrals"] = 0
        users_db[username]["balance"] += 1 # 1 ALB Bonus
        return {"status": "bonus_awarded", "count": 0}
    
    return {"status": "success", "count": users_db[username]["referrals"]}

@app.get("/holders")
async def get_holders():
    # Krijojmë listën e renditjes nga balanca më e madhe
    sorted_holders = []
    for user, data in users_db.items():
        sorted_holders.append({"name": user, "amount": data["balance"]})
    
    sorted_holders = sorted(sorted_holders, key=lambda x: x['amount'], reverse=True)
    return sorted_holders[:10] # Kthejmë 10 më të mirët
