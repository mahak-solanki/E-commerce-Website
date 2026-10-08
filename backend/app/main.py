from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os

from app.core.config import settings
from app.core.logging_config import configure_logging
from app.core.exceptions import register_exception_handlers
from app.middleware.request_logging import RequestLoggingMiddleware
from app.db.base import Base
from app.db.database import engine
from app.routers import products, categories, orders, auth, admin

configure_logging()

app = FastAPI(
    title=f"{settings.SHOP_NAME} API",
    description="Backend REST API for Annapurna Bhakti Bhandar — an e-commerce store for "
                 "women's accessories, certified Rudraksha, and Rashi Ratna bracelets.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(RequestLoggingMiddleware)

register_exception_handlers(app)

# Create tables automatically for convenience (in addition to Alembic migrations)
Base.metadata.create_all(bind=engine)

app.include_router(categories.router)
app.include_router(products.router)
app.include_router(orders.router)
app.include_router(auth.router)
app.include_router(admin.router)

# Serve locally hosted demo images
static_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "frontend", "static")
if os.path.isdir(static_dir):
    app.mount("/static", StaticFiles(directory=static_dir), name="static")

# Serve the frontend itself so the whole site can be opened from one server
frontend_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "frontend")
if os.path.isdir(frontend_dir):
    app.mount("/site", StaticFiles(directory=frontend_dir, html=True), name="site")


@app.get("/", tags=["Health"])
def root():
    return {
        "success": True,
        "message": f"Welcome to {settings.SHOP_NAME} API. Visit /docs for API documentation or /site for the website.",
        "data": {"docs": "/docs", "website": "/site/index.html"},
    }


@app.get("/api/config", tags=["Health"])
def public_config():
    """Public, non-sensitive shop configuration used by the frontend."""
    return {
        "success": True,
        "message": "Config fetched",
        "data": {
            "shop_name": settings.SHOP_NAME,
            "shop_phone": settings.SHOP_PHONE,
            "shop_email": settings.SHOP_EMAIL,
            "shop_address": settings.SHOP_ADDRESS,
            "whatsapp_number": settings.WHATSAPP_NUMBER,
            "delivery_charge": settings.DELIVERY_CHARGE,
            "free_delivery_above": settings.FREE_DELIVERY_ABOVE,
        },
    }
