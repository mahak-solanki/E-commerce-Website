import os
import sys
import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

os.environ["DATABASE_URL"] = "sqlite:///./test_annapurna.db"
os.environ["ADMIN_EMAIL"] = "admin@change-me.com"
os.environ["ADMIN_PASSWORD"] = "ChangeMe@123"

from fastapi.testclient import TestClient
from app.main import app
from app.db.database import SessionLocal, engine
from app.db.base import Base
from app.models.category import Category
from app.models.product import Product
from app.models.admin_user import AdminUser
from app.core.security import hash_password
from app.core.config import settings


@pytest.fixture(scope="session", autouse=True)
def setup_database():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        category = Category(name="Girls Collection", slug="girls-collection", description="Demo", is_active=True)
        db.add(category)
        db.commit()
        db.refresh(category)

        product = Product(
            name="Test Earrings", slug="test-earrings", description="A test product",
            price=500, discount_price=400, stock_quantity=10, image_url="",
            category_id=category.id, is_active=True, product_type="girls",
        )
        db.add(product)

        admin = AdminUser(
            email=settings.ADMIN_EMAIL, full_name="Admin",
            hashed_password=hash_password(settings.ADMIN_PASSWORD),
        )
        db.add(admin)
        db.commit()
    finally:
        db.close()
    yield
    Base.metadata.drop_all(bind=engine)
    if os.path.exists("./test_annapurna.db"):
        os.remove("./test_annapurna.db")


@pytest.fixture()
def client():
    return TestClient(app)


@pytest.fixture()
def admin_token(client):
    resp = client.post("/api/admin/login", json={"email": settings.ADMIN_EMAIL, "password": settings.ADMIN_PASSWORD})
    return resp.json()["data"]["access_token"]
