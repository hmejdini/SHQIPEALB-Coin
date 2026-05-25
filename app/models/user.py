from sqlalchemy import Column, Integer, String, Float
from app.core.database import Base

class User(Base):
    __tablename__ = "users"

    telegram_id = Column(Integer, primary_key=True, index=True)
    username = Column(String, nullable=True)
    first_name = Column(String)
    balance = Column(Integer, default=0)
    last_claim_time = Column(Float, default=0.0)
