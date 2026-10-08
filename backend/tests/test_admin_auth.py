from app.core.config import settings


def test_admin_login_success(client):
    resp = client.post("/api/admin/login", json={"email": settings.ADMIN_EMAIL, "password": settings.ADMIN_PASSWORD})
    assert resp.status_code == 200
    assert "access_token" in resp.json()["data"]


def test_admin_login_wrong_password(client):
    resp = client.post("/api/admin/login", json={"email": settings.ADMIN_EMAIL, "password": "wrongpass"})
    assert resp.status_code == 401


def test_unauthorized_admin_access(client):
    resp = client.get("/api/admin/dashboard")
    assert resp.status_code == 401


def test_admin_dashboard_with_valid_token(client, admin_token):
    resp = client.get("/api/admin/dashboard", headers={"Authorization": f"Bearer {admin_token}"})
    assert resp.status_code == 200
    assert "total_products" in resp.json()["data"]
