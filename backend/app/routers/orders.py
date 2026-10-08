from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.services import order_service
from app.schemas.order import OrderCreate, OrderOut

router = APIRouter(prefix="/api/orders", tags=["Orders"])


@router.post("", response_model=dict, status_code=201)
def place_order(payload: OrderCreate, db: Session = Depends(get_db)):
    order = order_service.create_order(db, payload)
    return {
        "success": True,
        "message": "Order placed successfully",
        "data": OrderOut.model_validate(order).model_dump(),
    }


@router.get("/{order_id}", response_model=dict)
def get_order(order_id: str, db: Session = Depends(get_db)):
    order = order_service.get_order_by_order_id(db, order_id)
    return {
        "success": True,
        "message": "Order fetched successfully",
        "data": OrderOut.model_validate(order).model_dump(),
    }
