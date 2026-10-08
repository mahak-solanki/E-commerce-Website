from sqlalchemy.orm import Session, joinedload

from app.models.order import Order, OrderStatus
from app.models.order_item import OrderItem
from app.models.product import Product
from app.schemas.order import OrderCreate
from app.core.exceptions import NotFoundException, BadRequestException
from app.core.config import settings

VALID_STATUSES = [s.value for s in OrderStatus]


def create_order(db: Session, data: OrderCreate) -> Order:
    if not data.items:
        raise BadRequestException("Cart cannot be empty")

    order_items = []
    subtotal = 0.0

    for item in data.items:
        product = db.query(Product).filter(Product.id == item.product_id).first()
        if not product or not product.is_active:
            raise NotFoundException(f"Product with id {item.product_id} not found")
        if product.stock_quantity < item.quantity:
            raise BadRequestException(
                f"Insufficient stock for '{product.name}'. Only {product.stock_quantity} left."
            )
        unit_price = product.discount_price if product.discount_price else product.price
        line_subtotal = round(unit_price * item.quantity, 2)
        subtotal += line_subtotal

        order_items.append(
            OrderItem(
                product_id=product.id,
                product_name_snapshot=product.name,
                product_image_snapshot=product.image_url,
                quantity=item.quantity,
                price=unit_price,
                subtotal=line_subtotal,
            )
        )
        product.stock_quantity -= item.quantity

    delivery_charge = 0.0 if subtotal >= settings.FREE_DELIVERY_ABOVE else settings.DELIVERY_CHARGE
    total = round(subtotal + delivery_charge, 2)

    address_line = f"{data.house_number}, {data.street}".strip(", ")

    order = Order(
        customer_name=data.customer_name,
        phone=data.phone,
        email=data.email or "",
        house_number=data.house_number,
        street=data.street,
        address=address_line,
        city=data.city,
        state=data.state,
        pincode=data.pincode,
        landmark=data.landmark or "",
        delivery_instructions=data.delivery_instructions or "",
        subtotal_amount=round(subtotal, 2),
        delivery_charge=delivery_charge,
        total_amount=total,
        payment_method="Cash on Delivery",
        items=order_items,
    )
    db.add(order)
    db.commit()
    db.refresh(order)
    return order


def get_order_by_order_id(db: Session, order_id: str) -> Order:
    order = (
        db.query(Order)
        .options(joinedload(Order.items))
        .filter(Order.order_id == order_id)
        .first()
    )
    if not order:
        raise NotFoundException("Order not found")
    return order


def list_orders(db: Session, status_filter: str | None = None):
    query = db.query(Order).options(joinedload(Order.items)).order_by(Order.created_at.desc())
    if status_filter:
        query = query.filter(Order.order_status == status_filter)
    return query.all()


def update_order_status(db: Session, order_id: str, new_status: str) -> Order:
    if new_status not in VALID_STATUSES:
        raise BadRequestException(f"Invalid status. Must be one of: {', '.join(VALID_STATUSES)}")
    order = get_order_by_order_id(db, order_id)
    order.order_status = new_status
    db.commit()
    db.refresh(order)
    return order
