from sqlalchemy import Column, Integer, Float, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.db.session import Base

class Payment(Base):
    __tablename__ = "payments"

    transaction_id = Column(Integer, primary_key=True, index=True)
    auction_id = Column(Integer, nullable=False)
    bidder_id = Column(Integer, nullable=False)
    amount = Column(Float, nullable=False)
    status = Column(String, default="pending")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
