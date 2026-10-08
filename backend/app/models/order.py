import enum
import uuid
from datetime import datetime
from sqlalchemy import String, DateTime, Float, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class OrderStatus(str, enum.Enum):
    PENDING = "Pending"
    CONFIRMED = "Confirmed"
    PACKED = "Packed"
    SHIPPED = "Shipped"
    OUT_FOR_DELIVERY = "Out for Delivery"
    DELIVERED = "Delivered"
    CANCELLED = "Cancelled"


class PaymentStatus(str, enum.Enum):
    PENDING = "Pending"
    PAID = "Paid"


def generate_order_id() -> str:
    return "ABB-" + uuid.uuid4().hex[:8].upper()


class Order(Base):
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(primary_key=True)
    order_id: Mapped[str] = mapped_column(String(50), unique=True, index=True, default=generate_order_id)

    customer_name: Mapped[str] = mapped_column(String(150), nullable=False)
    phone: Mapped[str] = mapped_column(String(20), nullable=False)
    email: Mapped[str] = mapped_column(String(255), nullable=True, default="")

    house_number: Mapped[str] = mapped_column(String(100), default="")
    street: Mapped[str] = mapped_column(String(255), default="")
    address: Mapped[str] = mapped_column(String(500), nullable=False)
    city: Mapped[str] = mapped_column(String(100), nullable=False)
    state: Mapped[str] = mapped_column(String(100), nullable=False)
    pincode: Mapped[str] = mapped_column(String(10), nullable=False)
    landmark: Mapped[str] = mapped_column(String(255), default="")
    delivery_instructions: Mapped[str] = mapped_column(String(500), default="")

    subtotal_amount: Mapped[float] = mapped_column(Float, default=0)
    delivery_charge: Mapped[float] = mapped_column(Float, default=0)
    total_amount: Mapped[float] = mapped_column(Float, nullable=False)

    payment_method: Mapped[str] = mapped_column(String(50), default="Cash on Delivery")
    payment_status: Mapped[str] = mapped_column(String(20), default=PaymentStatus.PENDING.value)
    order_status: Mapped[str] = mapped_column(String(30), default=OrderStatus.PENDING.value)

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    items = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")
