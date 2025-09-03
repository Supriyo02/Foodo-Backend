from fastapi import FastAPI
from contextlib import asynccontextmanager
from core.config.config import settings
from db.session import init_db_engine, shutdown_db
from application.vendors.routers import router as vendors_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    engine = init_db_engine(settings.DATABASE_URL)
    try:
        async with engine.begin() as conn:
            await conn.run_sync(lambda sync_conn: None)
    except Exception as exc:
        try:
            await shutdown_db()
        finally:
            print("Database startup check failed:", exc)
            raise

    print("Starting application.")
    try:
        yield
    finally:
        await shutdown_db
        print("Shutting down application.")

app = FastAPI(
    title="Foodo: The Homemade Food you deserve",
    version="0.1.0",
    lifespan=lifespan
)

app.include_router(vendors_router, prefix=f"{settings.ROUTER_PREFIX}/vendors", tags=["vendors"])