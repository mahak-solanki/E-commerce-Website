def test_product_retrieval(client):
    resp = client.get("/api/products")
    assert resp.status_code == 200
    data = resp.json()
    assert data["success"] is True
    assert data["data"]["total"] >= 1


def test_product_search(client):
    resp = client.get("/api/products?search=Earrings")
    assert resp.status_code == 200
    items = resp.json()["data"]["items"]
    assert any("Earrings" in p["name"] for p in items)


def test_product_search_no_results(client):
    resp = client.get("/api/products?search=NonExistentProductXYZ")
    assert resp.status_code == 200
    assert resp.json()["data"]["total"] == 0


def test_product_filtering_by_category(client):
    resp = client.get("/api/products?category=girls-collection")
    assert resp.status_code == 200
    items = resp.json()["data"]["items"]
    assert len(items) >= 1


def test_product_not_found(client):
    resp = client.get("/api/products/99999")
    assert resp.status_code == 404
    assert resp.json()["success"] is False


def test_product_creation_requires_admin(client):
    resp = client.post("/api/admin/products", json={
        "name": "New Product", "slug": "new-product", "price": 100,
        "stock_quantity": 5, "category_id": 1,
    })
    assert resp.status_code == 401


def test_product_creation_as_admin(client, admin_token):
    resp = client.post(
        "/api/admin/products",
        json={"name": "New Product", "slug": "new-product-1", "price": 100, "stock_quantity": 5, "category_id": 1},
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert resp.status_code == 201
    assert resp.json()["data"]["name"] == "New Product"
