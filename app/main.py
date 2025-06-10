import time
import logging

from fastapi import FastAPI, Request
from strawberry.fastapi import GraphQLRouter
from fastapi_cache.backends.inmemory import InMemoryBackend
from fastapi_cache import FastAPICache

from app.schema.schema import schema
from app.health import health_check
from prometheus_fastapi_instrumentator import Instrumentator
from app.db.session import engine, Base

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

start_time = time.time()
request_count = 0

app = FastAPI()

@app.middleware("http")
async def count_requests(request: Request, call_next):
    global request_count
    request_count += 1
    response = await call_next(request)
    return response

graphql_app = GraphQLRouter(schema)
app.include_router(graphql_app, prefix="/graphql")

instrumentator = Instrumentator()
instrumentator.instrument(app).expose(app)

@app.on_event("startup")
async def on_startup():
    FastAPICache.init(InMemoryBackend(), prefix="fastapi-cache")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    logger.info("Database tables created (if not exist)")

@app.get("/ping")
async def ping():
    logger.info("Ping called")
    return {"status": "ok"}

@app.get("/health")
async def health():
    logger.info("Health check called")
    return await health_check()

@app.get("/metrics-custom")
def metrics():
    return {
        "uptime_seconds": time.time() - start_time,
        "total_requests": request_count
    }
