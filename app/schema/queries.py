import strawberry
from typing import List, Optional
from sqlalchemy.future import select
from app.db.session import get_db_session
from app.db.models import Payment
from app.schema.types import PaymentType

@strawberry.type
class Query:

    @strawberry.field
    async def get_payments(self) -> List[PaymentType]:
        async with get_db_session() as session:
            result = await session.execute(select(Payment))
            payments = result.scalars().all()
            return [PaymentType(
                transaction_id=p.transaction_id,
                auction_id=p.auction_id,
                bidder_id=p.bidder_id,
                amount=p.amount,
                status=p.status,
                created_at=p.created_at
            ) for p in payments]

    @strawberry.field
    async def get_payment_by_id(self, transaction_id: int) -> Optional[PaymentType]:
        async with get_db_session() as session:
            result = await session.execute(select(Payment).filter_by(transaction_id=transaction_id))
            p = result.scalars().first()
            if p:
                return PaymentType(
                    transaction_id=p.transaction_id,
                    auction_id=p.auction_id,
                    bidder_id=p.bidder_id,
                    amount=p.amount,
                    status=p.status,
                    created_at=p.created_at
                )
            return None
