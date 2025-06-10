import strawberry
from sqlalchemy.future import select
from app.db.session import get_db_session
from app.db.models import Payment
from app.schema.types import PaymentType, PaymentInput
from notif import send_notification_message

@strawberry.type
class Mutation:

    @strawberry.mutation
    async def create_payment(self, payment_input: PaymentInput) -> PaymentType:
        async with get_db_session() as session:
            new_payment = Payment(
                auction_id=payment_input.auction_id,
                bidder_id=payment_input.bidder_id,
                amount=payment_input.amount,
                status="pending"
            )
            session.add(new_payment)
            await send_notification_message({
                "type": "payment_loaded",
                "amount": new_payment.amount,
                "timestamp": str(new_payment.created_at)
            })

            await session.commit()
            await session.refresh(new_payment)

            return PaymentType(
                transaction_id=new_payment.transaction_id,
                auction_id=new_payment.auction_id,
                bidder_id=new_payment.bidder_id,
                amount=new_payment.amount,
                status=new_payment.status,
                created_at=new_payment.created_at
            )
