def _get_first_product_id(client):
    resp = client.get("/api/products?page_size=1")
    return resp.json()["data"]["items"][0]["id"]


def test_order_creation(client):
    pid = _get_first_product_id(client)
    resp = client.post("/api/orders", json={
        "customer_name": "Test User", "phone": "9876543210", "email": "",
        "house_number": "12", "street": "MG Road", "city": "Indore", "state": "MP",
        "pincode": "452001", "items": [{"product_id": pid, "quantity": 1}],
    })
    assert resp.status_code == 201
    data = resp.json()["data"]
    assert data["order_id"].startswith("ABB-")
    assert data["order_status"] == "Pending"


def test_invalid_order_bad_pincode(client):
    pid = _get_first_product_id(client)
    resp = client.post("/api/orders", json={
        "customer_name": "Bad User", "phone": "9876543210", "house_number": "1",
        "street": "X", "city": "Y", "state": "Z", "pincode": "12",
        "items": [{"product_id": pid, "quantity": 1}],
    })
    assert resp.status_code == 422


def test_invalid_order_empty_cart(client):
    resp = client.post("/api/orders", json={
        "customer_name": "Bad User", "phone": "9876543210", "house_number": "1",
        "street": "X", "city": "Y", "state": "Z", "pincode": "452001", "items": [],
    })
    assert resp.status_code == 422


def test_stock_validation(client):
    pid = _get_first_product_id(client)
    resp = client.post("/api/orders", json={
        "customer_name": "Greedy User", "phone": "9876543210", "house_number": "1",
        "street": "X", "city": "Y", "state": "Z", "pincode": "452001",
        "items": [{"product_id": pid, "quantity": 999999}],
    })
    assert resp.status_code == 400


def test_order_status_update(client, admin_token):
    pid = _get_first_product_id(client)
    order_resp = client.post("/api/orders", json={
        "customer_name": "Status User", "phone": "9876543210", "house_number": "1",
        "street": "X", "city": "Y", "state": "Z", "pincode": "452001",
        "items": [{"product_id": pid, "quantity": 1}],
    })
    order_id = order_resp.json()["data"]["order_id"]

    resp = client.put(
        f"/api/admin/orders/{order_id}/status",
        json={"order_status": "Confirmed"},
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert resp.status_code == 200
    assert resp.json()["data"]["order_status"] == "Confirmed"


def test_order_status_update_requires_admin(client):
    resp = client.put("/api/admin/orders/ABB-FAKE1234/status", json={"order_status": "Confirmed"})
    assert resp.status_code == 401
