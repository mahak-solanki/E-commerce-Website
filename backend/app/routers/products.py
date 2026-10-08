from typing import Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.services import product_service
from app.schemas.product import ProductOut

router = APIRouter(prefix="/api/products", tags=["Products"])


@router.get("", response_model=dict)
def get_products(
    category: Optional[str] = Query(None, description="Category slug"),
    product_type: Optional[str] = Query(None),
    rashi: Optional[str] = Query(None),
    mukhi: Optional[str] = Query(None),
    search: Optional[str] = Query(None),
    min_price: Optional[float] = Query(None),
    max_price: Optional[float] = Query(None),
    in_stock_only: bool = Query(False),
    sort: Optional[str] = Query(None, description="price_asc|price_desc|name_asc|newest"),
    page: int = Query(1, ge=1),
    page_size: int = Query(12, ge=1, le=100),
    db: Session = Depends(get_db),
):
    items, total, page, pages = product_service.list_products(
        db,
        category_slug=category,
        product_type=product_type,
        rashi=rashi,
        mukhi=mukhi,
        search=search,
        min_price=min_price,
        max_price=max_price,
        in_stock_only=in_stock_only,
        sort=sort,
        page=page,
        page_size=page_size,
    )
    return {
        "success": True,
        "message": "Products fetched successfully",
        "data": {
            "items": [ProductOut.model_validate(p).model_dump() for p in items],
            "total": total,
            "page": page,
            "page_size": page_size,
            "pages": pages,
        },
    }


@router.get("/slug/{slug}", response_model=dict)
def get_product_by_slug(slug: str, db: Session = Depends(get_db)):
    product = product_service.get_product_by_slug(db, slug)
    return {
        "success": True,
        "message": "Product fetched successfully",
        "data": ProductOut.model_validate(product).model_dump(),
    }


@router.get("/{product_id}", response_model=dict)
def get_product(product_id: int, db: Session = Depends(get_db)):
    product = product_service.get_product(db, product_id)
    return {
        "success": True,
        "message": "Product fetched successfully",
        "data": ProductOut.model_validate(product).model_dump(),
    }
