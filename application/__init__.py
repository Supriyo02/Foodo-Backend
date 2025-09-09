from fastapi import FastAPI
from contextlib import asynccontextmanager
from core.config.config import settings
from db.session import init_db_engine, shutdown_db
from application.vendor.routers import router as vendor_routers
from application.user.routers import router as user_routers
from application.menu.routers import router as menu_router
from fastapi.responses import JSONResponse


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

app.include_router(vendor_routers, prefix=f"{settings.ROUTER_PREFIX}/vendors", tags=["vendors"])
app.include_router(user_routers, prefix=f"{settings.ROUTER_PREFIX}/users", tags=["users"])
app.include_router(menu_router, prefix=f"{settings.ROUTER_PREFIX}/menus", tags=["menus"])

@app.get("/health", response_class=JSONResponse, tags=["health"])
async def health():
    return {"status": "ok"}