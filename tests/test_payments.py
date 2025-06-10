import pytest
from httpx import AsyncClient
from app.main import app

@pytest.mark.asyncio
async def test_graphql_create_payment():
    mutation = """
    mutation {
        createPayment(paymentInput: {
            auctionId: 1,
            bidderId: 1,
            amount: 99.99
        }) {
            transactionId
            auctionId
            bidderId
            amount
            status
            createdAt
        }
    }
    """
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post("/graphql", json={"query": mutation})
        assert response.status_code == 200
        data = response.json()
        assert "data" in data
        assert "createPayment" in data["data"]

