# 🕉️ Annapurna Bhakti Bhandar — E-Commerce Platform

A complete, production-style e-commerce website for **Annapurna Bhakti Bhandar** — a shop
selling Girls/Women's accessories, Certified Rudraksha, and Rashi Ratna gemstone bracelets,
with home delivery and Cash on Delivery payment.

---

## 1. Project Overview

Customers can browse three product categories, search & filter, add items to a cart,
check out with a delivery address, and place a Cash-on-Delivery order. The shop owner
manages products, categories, and orders through a secured admin panel.

## 2. Features

- Beautiful, responsive, spiritual/feminine Indian-themed UI (no frontend framework — plain HTML/CSS/JS + Axios-style fetch wrapper)
- Product browsing, search, filtering (category, price, Rashi, Mukhi, stock) and sorting
- Product detail pages with category-specific specs
- Cart with quantity management (guest cart via localStorage)
- Checkout with full delivery-address form and client + server side validation
- Order placement, confirmation page with Order ID, Cash on Delivery
- Admin panel: dashboard stats, product CRUD, category CRUD, order status management
- JWT-secured admin API, bcrypt password hashing
- Clean layered FastAPI backend (routers → services → models)
- Consistent `{success, message, data}` API responses & centralized error handling
- Alembic migrations + seed script with realistic demo data
- Pytest test suite (17 tests covering products, orders, and admin auth)
- Docker & docker-compose (FastAPI + PostgreSQL)

## 3. Tech Stack

**Backend:** Python 3.13, FastAPI, SQLAlchemy 2.x, PostgreSQL (SQLite by default for quick
start), Pydantic v2, Alembic, Uvicorn, python-jose/PyJWT, Passlib/bcrypt, pytest

**Frontend:** HTML, CSS, vanilla JavaScript (fetch-based API client). No React.

## 4. Architecture

```
backend/
├── app/
│   ├── main.py                # FastAPI app, CORS, routers, static mounts
│   ├── core/                  # config, security, logging, exception handling
│   ├── db/                    # engine/session/base
│   ├── models/                # SQLAlchemy models
│   ├── schemas/                # Pydantic v2 schemas
│   ├── routers/                # API endpoints (thin controllers)
│   ├── services/                # business logic
│   ├── dependencies/            # auth dependency
│   └── middleware/              # request logging
├── frontend/                  # static HTML/CSS/JS site (served at /site)
│   ├── index.html, products.html, product-detail.html, cart.html,
│   │   checkout.html, order-success.html, login.html
│   ├── admin/ (dashboard.html, products.html, orders.html)
│   ├── css/style.css
│   ├── js/ (api.js, cart.js, layout.js, admin.js)
│   └── static/images/ (local SVG placeholder images)
├── alembic/                   # migrations
├── tests/                     # pytest suite
├── seed.py                    # demo data seeder
├── requirements.txt
├── Dockerfile / docker-compose.yml
└── .env.example
```

## 5. Folder Structure

See section 4 above — matches the requested layout.

## 6. Installation

```bash
cd backend
python3 -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env          # then edit .env — see section 7
```

## 7. Environment Variables

Copy `.env.example` to `.env` and fill in real values. See section 17 (below) for the
full "must change before deployment" checklist.

## 8. Database Setup

**Quick start (SQLite, zero setup):** the default `DATABASE_URL` in `.env.example`
already points to a local SQLite file — no extra steps needed for local testing.

**PostgreSQL (recommended for production):**

```bash
# Example using Docker for just the DB:
docker run --name annapurna-pg -e POSTGRES_USER=annapurna \
  -e POSTGRES_PASSWORD=annapurna_change_me -e POSTGRES_DB=annapurna_db \
  -p 5432:5432 -d postgres:16-alpine

# Then in .env:
DATABASE_URL=postgresql://annapurna:annapurna_change_me@localhost:5432/annapurna_db
```

## 9. Alembic Migration

```bash
cd backend
alembic upgrade head
# To create a new migration after changing models:
alembic revision --autogenerate -m "describe your change"
```

(Note: `app/main.py` also calls `Base.metadata.create_all()` on startup for convenience,
so the app will run even without migrations. Alembic is the recommended path for
production schema changes.)

## 10. Seed Demo Data

```bash
python seed.py
```

This creates the 3 categories, 12+ Girls Collection products, 15 Rudraksha products
(all 12 Mukhi types + mala + bracelet + combo), and 12 Rashi Ratna bracelets (one per
Rashi), plus the initial admin user from `ADMIN_EMAIL` / `ADMIN_PASSWORD`.

> ⚠️ These are DEMO products/prices and should be replaced with real shop inventory
> before production use.

## 11. Running the Backend

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## 12. Running the Frontend

The FastAPI app itself serves the static frontend at **`http://localhost:8000/site/index.html`**
— no separate server needed. (It also serves demo images at `/static/images/...`.)

If you prefer to serve the frontend separately (e.g. `python -m http.server` inside
`frontend/`), it will still work — `js/api.js` auto-detects the API origin.

## 13. API Documentation

Interactive Swagger docs: **`http://localhost:8000/docs`**
ReDoc: **`http://localhost:8000/redoc`**

Key endpoints:
```
GET    /api/categories
GET    /api/categories/{id}
GET    /api/products                 (search, filter, sort, pagination via query params)
GET    /api/products/{id}
GET    /api/products/slug/{slug}
POST   /api/orders
GET    /api/orders/{order_id}
POST   /api/admin/login
GET    /api/admin/dashboard          (protected)
GET/POST/PUT/DELETE /api/admin/products  (protected)
POST/PUT /api/admin/categories           (protected)
GET    /api/admin/orders                 (protected)
PUT    /api/admin/orders/{order_id}/status (protected)
```

## 14. Admin Login Setup

1. Set `ADMIN_EMAIL` / `ADMIN_PASSWORD` in `.env`.
2. Run `python seed.py` (creates the admin user with a bcrypt-hashed password).
3. Visit `/site/login.html`, log in, and you're redirected to `/site/admin/dashboard.html`.

## 15. Changing Products

Use the Admin Panel → **Products** page (Add / Edit / Deactivate), or edit `seed.py`
and re-run it (it upserts by slug, so re-running is safe).

## 16. Changing Product Images

Edit the `image_url` field on each product (via Admin Panel or `seed.py`). Any broken
image automatically falls back to a local placeholder SVG in
`frontend/static/images/placeholder-*.svg` — replace these files with your own branded
placeholders if you like.

## 17. 🔴 YOU MUST CHANGE THESE BEFORE REAL USE

| # | Setting | Where to change it |
|---|---------|---------------------|
| 1 | `DATABASE_URL` | `.env` |
| 2 | `SECRET_KEY` | `.env` (use a long random string) |
| 3 | `ADMIN_EMAIL` | `.env`, then re-run `python seed.py` |
| 4 | `ADMIN_PASSWORD` | `.env`, then re-run `python seed.py` |
| 5 | `SHOP_PHONE` | `.env` |
| 6 | `SHOP_EMAIL` | `.env` |
| 7 | `WHATSAPP_NUMBER` | `.env` (international format, digits only, e.g. `9198xxxxxxx`) |
| 8 | `SHOP_ADDRESS` | `.env` |
| 9 | `DELIVERY_CHARGE` | `.env` |
| 10 | `FREE_DELIVERY_ABOVE` | `.env` |
| 11 | Product images | Admin Panel → Products, or `seed.py` |
| 12 | Product prices | Admin Panel → Products, or `seed.py` |
| 13 | Product stock | Admin Panel → Products, or `seed.py` |
| 14 | Shop logo | Replace `frontend/static/images/hero-banner.svg` and the 🕉️ emoji brand mark in `frontend/js/layout.js` |
| 15 | Social media links | `frontend/js/layout.js` → `renderFooter()` (the `#` placeholders in `social-row`) |

## 18. Deployment

The backend is a standard FastAPI app and can be deployed to:

- **Render / Railway:** point to `backend/`, build command `pip install -r requirements.txt`,
  start command `uvicorn app.main:app --host 0.0.0.0 --port $PORT`. Add a managed
  PostgreSQL add-on and set `DATABASE_URL` accordingly.
- **VPS:** run behind Nginx + gunicorn/uvicorn workers, or use the provided Dockerfile.
- **Docker:** `docker compose up --build` runs both the API and a PostgreSQL database.

Vercel is not a good fit here — this is a stateful FastAPI + PostgreSQL app, not a
serverless-friendly framework, and Vercel's Python runtime does not support long-lived
DB connections and background processes the way this app is built. Render/Railway/VPS/Docker
are recommended instead.

## 19. Testing

```bash
cd backend
pytest tests/ -v
```

17 tests cover: product creation/retrieval/search/filtering, order creation, invalid
orders (bad pincode, empty cart), stock validation, admin login (success/failure),
unauthorized admin access, and order status updates.

**Manual end-to-end checklist:**
Homepage → Browse category → Product detail → Add to cart → Cart → Checkout (fill
delivery form) → Place Order → Order confirmation with Order ID → Admin login →
Admin dashboard → Admin sees the new order → Admin updates order status.

## 20. Future Improvements

- Online payment (Razorpay/UPI) — the codebase is structured so a `payment_method`
  field and `PaymentStatus` enum already exist; add a new service module
  (`services/payment_service.py`) and a webhook route to complete integration.
- Product image upload (currently URL-based)
- Customer accounts / order history by phone or email
- Email/SMS order notifications
- Product reviews and ratings
- Multi-admin roles/permissions

---

## Docker Quick Start

```bash
cd backend
cp .env.example .env   # optional, docker-compose.yml has working defaults for local testing
docker compose up --build
```

Then visit `http://localhost:8000/site/index.html` (storefront) and
`http://localhost:8000/docs` (API docs). The container automatically seeds demo data
on first boot.

---

**Demo storefront disclaimer:** All product prices, WhatsApp numbers, phone numbers,
emails, and addresses in this repository are placeholders (`CHANGE_ME`) or demo values
and must be replaced with real business information before going live.
