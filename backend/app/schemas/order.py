import re
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict, EmailStr, field_validator


class OrderItemIn(BaseModel):
    product_id: int
    quantity: int

    @field_validator("quantity")
    @classmethod
    def qty_positive(cls, v):
        if v <= 0:
            raise ValueError("quantity must be at least 1")
        return v


class OrderItemOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    product_id: int
    product_name_snapshot: str
    product_image_snapshot: str
    quantity: int
    price: float
    subtotal: float


class OrderCreate(BaseModel):
    customer_name: str
    phone: str
    email: Optional[str] = ""
    house_number: str
    street: str
    city: str
    state: str
    pincode: str
    landmark: Optional[str] = ""
    delivery_instructions: Optional[str] = ""
    items: list[OrderItemIn]

    @field_validator("customer_name")
    @classmethod
    def name_not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError("Full name is required")
        return v.strip()

    @field_validator("phone")
    @classmethod
    def phone_valid(cls, v):
        digits = re.sub(r"\D", "", v or "")
        if len(digits) != 10:
            raise ValueError("Mobile number must be a valid 10 digit number")
        return digits

    @field_validator("pincode")
    @classmethod
    def pincode_valid(cls, v):
        if not re.fullmatch(r"\d{6}", v or ""):
            raise ValueError("Pincode must be a valid 6 digit number")
        return v

    @field_validator("email")
    @classmethod
    def email_optional_valid(cls, v):
        if v:
            if not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", v):
                raise ValueError("Email is not valid")
        return v

    @field_validator("items")
    @classmethod
    def items_not_empty(cls, v):
        if not v:
            raise ValueError("Cart cannot be empty")
        return v


class OrderStatusUpdate(BaseModel):
    order_status: str


class OrderOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    order_id: str
    customer_name: str
    phone: str
    email: Optional[str] = ""
    house_number: str
    street: str
    address: str
    city: str
    state: str
    pincode: str
    landmark: Optional[str] = ""
    delivery_instructions: Optional[str] = ""
    subtotal_amount: float
    delivery_charge: float
    total_amount: float
    payment_method: str
    payment_status: str
    order_status: str
    created_at: datetime
    updated_at: datetime
    items: list[OrderItemOut]
