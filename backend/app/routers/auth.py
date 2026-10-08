from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.services.auth_service import authenticate_admin
from app.schemas.admin import AdminLogin

router = APIRouter(prefix="/api/admin", tags=["Admin Auth"])


@router.post("/login", response_model=dict)
def admin_login(payload: AdminLogin, db: Session = Depends(get_db)):
    token = authenticate_admin(db, payload.email, payload.password)
    return {
        "success": True,
        "message": "Login successful",
        "data": {"access_token": token, "token_type": "bearer"},
    }
