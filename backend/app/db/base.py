from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


# Import all models here so Alembic autogenerate and Base.metadata.create_all
# can discover them.
from app.models.category import Category  # noqa
from app.models.product import Product  # noqa
from app.models.admin_user import AdminUser  # noqa
from app.models.order import Order  # noqa
from app.models.order_item import OrderItem  # noqa
