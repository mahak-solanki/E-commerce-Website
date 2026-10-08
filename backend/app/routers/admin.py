from typing import Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.db.session import get_db
from app.dependencies.auth import get_current_admin
from app.models.admin_user import AdminUser
from app.models.product import Product
from app.models.order import Order, OrderStatus
from app.models.category import Category
from app.schemas.product import ProductCreate, ProductUpdate, ProductOut
from app.schemas.category import CategoryCreate, CategoryUpdate, CategoryOut
from app.schemas.order import OrderOut, OrderStatusUpdate
from app.schemas.admin import DashboardStats
from app.services import product_service, order_service
from app.core.exceptions import BadRequestException

router = APIRouter(prefix="/api/admin", tags=["Admin"])


@router.get("/dashboard", response_model=dict)
def dashboard(db: Session = Depends(get_db), admin: AdminUser = Depends(get_current_admin)):
    total_products = db.query(func.count(Product.id)).filter(Product.is_active == True).scalar()  # noqa
    total_orders = db.query(func.count(Order.id)).scalar()
    pending_orders = (
        db.query(func.count(Order.id))
        .filter(Order.order_status == OrderStatus.PENDING.value)
        .scalar()
    )
    delivered_orders = (
        db.query(func.count(Order.id))
        .filter(Order.order_status == OrderStatus.DELIVERED.value)
        .scalar()
    )
    total_sales = db.query(func.coalesce(func.sum(Order.total_amount), 0.0)).filter(
        Order.order_status != OrderStatus.CANCELLED.value
    ).scalar()

    stats = DashboardStats(
        total_products=total_products or 0,
        total_orders=total_orders or 0,
        pending_orders=pending_orders or 0,
        delivered_orders=delivered_orders or 0,
        total_sales=float(total_sales or 0),
    )
    return {"success": True, "message": "Dashboard stats fetched", "data": stats.model_dump()}


# ---------- Product management ----------

@router.post("/products", response_model=dict, status_code=201)
def admin_create_product(
    payload: ProductCreate,
    db: Session = Depends(get_db),
    admin: AdminUser = Depends(get_current_admin),
):
    product = product_service.create_product(db, payload)
    return {"success": True, "message": "Product created", "data": ProductOut.model_validate(product).model_dump()}


@router.get("/products", response_model=dict)
def admin_list_products(
    page: int = Query(1, ge=1),
    page_size: int = Query(50, ge=1, le=200),
    db: Session = Depends(get_db),
    admin: AdminUser = Depends(get_current_admin),
):
    items, total, page, pages = product_service.list_products(
        db, page=page, page_size=page_size, include_inactive=True
    )
    return {
        "success": True,
        "message": "Products fetched",
        "data": {
            "items": [ProductOut.model_validate(p).model_dump() for p in items],
            "total": total, "page": page, "page_size": page_size, "pages": pages,
        },
    }


@router.put("/products/{product_id}", response_model=dict)
def admin_update_product(
    product_id: int,
    payload: ProductUpdate,
    db: Session = Depends(get_db),
    admin: AdminUser = Depends(get_current_admin),
):
    product = product_service.update_product(db, product_id, payload)
    return {"success": True, "message": "Product updated", "data": ProductOut.model_validate(product).model_dump()}


@router.delete("/products/{product_id}", response_model=dict)
def admin_delete_product(
    product_id: int,
    db: Session = Depends(get_db),
    admin: AdminUser = Depends(get_current_admin),
):
    product_service.delete_product(db, product_id)
    return {"success": True, "message": "Product deactivated", "data": None}


# ---------- Category management ----------

@router.post("/categories", response_model=dict, status_code=201)
def admin_create_category(
    payload: CategoryCreate,
    db: Session = Depends(get_db),
    admin: AdminUser = Depends(get_current_admin),
):
    existing = db.query(Category).filter(Category.slug == payload.slug).first()
    if existing:
        raise BadRequestException("A category with this slug already exists")
    category = Category(**payload.model_dump())
    db.add(category)
    db.commit()
    db.refresh(category)
    return {"success": True, "message": "Category created", "data": CategoryOut.model_validate(category).model_dump()}


@router.put("/categories/{category_id}", response_model=dict)
def admin_update_category(
    category_id: int,
    payload: CategoryUpdate,
    db: Session = Depends(get_db),
    admin: AdminUser = Depends(get_current_admin),
):
    category = db.query(Category).filter(Category.id == category_id).first()
    if not category:
        raise BadRequestException("Category not found")
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(category, field, value)
    db.commit()
    db.refresh(category)
    return {"success": True, "message": "Category updated", "data": CategoryOut.model_validate(category).model_dump()}


# ---------- Order management ----------

@router.get("/orders", response_model=dict)
def admin_list_orders(
    status_filter: Optional[str] = Query(None, alias="status"),
    db: Session = Depends(get_db),
    admin: AdminUser = Depends(get_current_admin),
):
    orders = order_service.list_orders(db, status_filter)
    return {
        "success": True,
        "message": "Orders fetched",
        "data": [OrderOut.model_validate(o).model_dump() for o in orders],
    }


@router.get("/orders/{order_id}", response_model=dict)
def admin_get_order(
    order_id: str,
    db: Session = Depends(get_db),
    admin: AdminUser = Depends(get_current_admin),
):
    order = order_service.get_order_by_order_id(db, order_id)
    return {"success": True, "message": "Order fetched", "data": OrderOut.model_validate(order).model_dump()}


@router.put("/orders/{order_id}/status", response_model=dict)
def admin_update_order_status(
    order_id: str,
    payload: OrderStatusUpdate,
    db: Session = Depends(get_db),
    admin: AdminUser = Depends(get_current_admin),
):
    order = order_service.update_order_status(db, order_id, payload.order_status)
    return {"success": True, "message": "Order status updated", "data": OrderOut.model_validate(order).model_dump()}
