import strawberry
from datetime import datetime

@strawberry.type
class PaymentType:
    transaction_id: int
    auction_id: int
    bidder_id: int
    amount: float
    status: str
    created_at: datetime

@strawberry.input
class PaymentInput:
    auction_id: int
    bidder_id: int
    amount: float