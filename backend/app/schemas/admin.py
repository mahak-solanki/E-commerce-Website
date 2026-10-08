from pydantic import BaseModel


class AdminLogin(BaseModel):
    email: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class DashboardStats(BaseModel):
    total_products: int
    total_orders: int
    pending_orders: int
    delivered_orders: int
    total_sales: float
