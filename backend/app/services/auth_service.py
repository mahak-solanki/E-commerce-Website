from sqlalchemy.orm import Session

from app.models.admin_user import AdminUser
from app.core.security import verify_password, create_access_token
from app.core.exceptions import UnauthorizedException


def authenticate_admin(db: Session, email: str, password: str) -> str:
    admin = db.query(AdminUser).filter(AdminUser.email == email).first()
    if not admin or not verify_password(password, admin.hashed_password):
        raise UnauthorizedException("Invalid email or password")
    token = create_access_token({"sub": admin.email})
    return token
