import math
from typing import Optional
from sqlalchemy import or_, asc, desc
from sqlalchemy.orm import Session

from app.models.product import Product
from app.schemas.product import ProductCreate, ProductUpdate
from app.core.exceptions import NotFoundException, BadRequestException


def list_products(
    db: Session,
    category_slug: Optional[str] = None,
    product_type: Optional[str] = None,
    rashi: Optional[str] = None,
    mukhi: Optional[str] = None,
    search: Optional[str] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    in_stock_only: bool = False,
    sort: Optional[str] = None,
    page: int = 1,
    page_size: int = 12,
    include_inactive: bool = False,
):
    query = db.query(Product)
    if not include_inactive:
        query = query.filter(Product.is_active == True)  # noqa: E712

    if category_slug:
        query = query.join(Product.category).filter_by(slug=category_slug)
    if product_type:
        query = query.filter(Product.product_type == product_type)
    if rashi:
        query = query.filter(Product.rashi == rashi)
    if mukhi:
        query = query.filter(Product.mukhi == mukhi)
    if search:
        like = f"%{search}%"
        query = query.filter(or_(Product.name.ilike(like), Product.description.ilike(like)))
    if min_price is not None:
        query = query.filter(Product.price >= min_price)
    if max_price is not None:
        query = query.filter(Product.price <= max_price)
    if in_stock_only:
        query = query.filter(Product.stock_quantity > 0)

    if sort == "price_asc":
        query = query.order_by(asc(Product.price))
    elif sort == "price_desc":
        query = query.order_by(desc(Product.price))
    elif sort == "name_asc":
        query = query.order_by(asc(Product.name))
    else:
        query = query.order_by(desc(Product.created_at))

    total = query.count()
    pages = max(1, math.ceil(total / page_size))
    page = max(1, min(page, pages))
    items = query.offset((page - 1) * page_size).limit(page_size).all()
    return items, total, page, pages


def get_product(db: Session, product_id: int) -> Product:
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise NotFoundException("Product not found")
    return product


def get_product_by_slug(db: Session, slug: str) -> Product:
    product = db.query(Product).filter(Product.slug == slug).first()
    if not product:
        raise NotFoundException("Product not found")
    return product


def create_product(db: Session, data: ProductCreate) -> Product:
    existing = db.query(Product).filter(Product.slug == data.slug).first()
    if existing:
        raise BadRequestException("A product with this slug already exists")
    product = Product(**data.model_dump())
    db.add(product)
    db.commit()
    db.refresh(product)
    return product


def update_product(db: Session, product_id: int, data: ProductUpdate) -> Product:
    product = get_product(db, product_id)
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(product, field, value)
    db.commit()
    db.refresh(product)
    return product


def delete_product(db: Session, product_id: int) -> None:
    product = get_product(db, product_id)
    product.is_active = False
    db.commit()
