from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.category import Category
from app.schemas.category import CategoryOut
from app.core.exceptions import NotFoundException

router = APIRouter(prefix="/api/categories", tags=["Categories"])


@router.get("", response_model=dict)
def get_categories(db: Session = Depends(get_db)):
    categories = db.query(Category).filter(Category.is_active == True).all()  # noqa: E712
    return {
        "success": True,
        "message": "Categories fetched successfully",
        "data": [CategoryOut.model_validate(c).model_dump() for c in categories],
    }


@router.get("/{category_id}", response_model=dict)
def get_category(category_id: int, db: Session = Depends(get_db)):
    category = db.query(Category).filter(Category.id == category_id).first()
    if not category:
        raise NotFoundException("Category not found")
    return {
        "success": True,
        "message": "Category fetched successfully",
        "data": CategoryOut.model_validate(category).model_dump(),
    }
