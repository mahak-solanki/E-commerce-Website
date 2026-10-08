from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict, field_validator


class ProductBase(BaseModel):
    name: str
    slug: str
    description: Optional[str] = ""
    price: float
    discount_price: Optional[float] = None
    stock_quantity: int = 0
    image_url: Optional[str] = ""
    category_id: int
    is_active: bool = True
    product_type: Optional[str] = None
    rashi: Optional[str] = None
    mukhi: Optional[str] = None
    gemstone: Optional[str] = None
    certification: Optional[str] = None
    size: Optional[str] = None
    material: Optional[str] = None
    color: Optional[str] = None

    @field_validator("price")
    @classmethod
    def price_positive(cls, v):
        if v is None or v < 0:
            raise ValueError("price must be a positive number")
        return v

    @field_validator("stock_quantity")
    @classmethod
    def stock_non_negative(cls, v):
        if v < 0:
            raise ValueError("stock_quantity cannot be negative")
        return v


class ProductCreate(ProductBase):
    pass


class ProductUpdate(BaseModel):
    name: Optional[str] = None
    slug: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    discount_price: Optional[float] = None
    stock_quantity: Optional[int] = None
    image_url: Optional[str] = None
    category_id: Optional[int] = None
    is_active: Optional[bool] = None
    product_type: Optional[str] = None
    rashi: Optional[str] = None
    mukhi: Optional[str] = None
    gemstone: Optional[str] = None
    certification: Optional[str] = None
    size: Optional[str] = None
    material: Optional[str] = None
    color: Optional[str] = None


class ProductOut(ProductBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    created_at: datetime
    updated_at: datetime


class PaginatedProducts(BaseModel):
    items: list[ProductOut]
    total: int
    page: int
    page_size: int
    pages: int
