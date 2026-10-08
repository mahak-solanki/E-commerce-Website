from fastapi import Depends, Header
from sqlalchemy.orm import Session
import jwt

from app.db.session import get_db
from app.core.security import decode_access_token
from app.core.exceptions import UnauthorizedException
from app.models.admin_user import AdminUser


def get_current_admin(
    authorization: str = Header(default=None),
    db: Session = Depends(get_db),
) -> AdminUser:
    if not authorization or not authorization.lower().startswith("bearer "):
        raise UnauthorizedException("Missing or invalid authorization header")

    token = authorization.split(" ", 1)[1]
    try:
        payload = decode_access_token(token)
    except jwt.ExpiredSignatureError:
        raise UnauthorizedException("Session expired. Please log in again.")
    except jwt.InvalidTokenError:
        raise UnauthorizedException("Invalid authentication token")

    email = payload.get("sub")
    if not email:
        raise UnauthorizedException("Invalid authentication token")

    admin = db.query(AdminUser).filter(AdminUser.email == email).first()
    if not admin:
        raise UnauthorizedException("Admin account not found")
    return admin
