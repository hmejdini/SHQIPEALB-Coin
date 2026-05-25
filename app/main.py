from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import coins
from app.core.database import init_db
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Kjo krijon automatikisht databazën kur ndizet serveri për herë të parë
    await init_db()
    yield

app = FastAPI(title="AlbCoin Backend", lifespan=lifespan)

# Lejon komunikimin pa bllokime me frontend-in tënd në GitHub Pages
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(coins.router)

@app.get("/")
def health_check():
    return {"status": "AlbCoin Backend online!"}
