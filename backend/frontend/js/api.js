// ---------------------------------------------------------------
// API base configuration
// If the site is opened via the FastAPI-served /site path, the API
// lives on the same origin. Otherwise it defaults to localhost:8000
// (useful when opening the HTML files directly during development).
// ---------------------------------------------------------------
const API_BASE = window.location.origin.includes("file://")
  ? "http://localhost:8000"
  : window.location.origin;

const FALLBACK_IMAGE = "/static/images/placeholder-generic.svg";

async function apiRequest(path, options = {}) {
  const url = `${API_BASE}${path}`;
  const headers = options.headers || {};
  if (!(options.body instanceof FormData) && options.body) {
    headers["Content-Type"] = "application/json";
  }
  const token = localStorage.getItem("abb_admin_token");
  if (token && path.startsWith("/api/admin")) {
    headers["Authorization"] = `Bearer ${token}`;
  }
  const res = await fetch(url, { ...options, headers });
  let json;
  try {
    json = await res.json();
  } catch (e) {
    throw new Error("Unexpected server response");
  }
  if (!res.ok || json.success === false) {
    const err = new Error(json.message || "Something went wrong");
    err.status = res.status;
    err.data = json.data;
    throw err;
  }
  return json.data;
}

const api = {
  getCategories: () => apiRequest("/api/categories"),
  getProducts: (params = {}) => {
    const qs = new URLSearchParams(
      Object.entries(params).filter(([, v]) => v !== undefined && v !== null && v !== "")
    ).toString();
    return apiRequest(`/api/products${qs ? "?" + qs : ""}`);
  },
  getProduct: (id) => apiRequest(`/api/products/${id}`),
  getProductBySlug: (slug) => apiRequest(`/api/products/slug/${slug}`),
  placeOrder: (payload) => apiRequest("/api/orders", { method: "POST", body: JSON.stringify(payload) }),
  getOrder: (orderId) => apiRequest(`/api/orders/${orderId}`),
  getConfig: () => apiRequest("/api/config"),

  adminLogin: (email, password) =>
    apiRequest("/api/admin/login", { method: "POST", body: JSON.stringify({ email, password }) }),
  adminDashboard: () => apiRequest("/api/admin/dashboard"),
  adminListProducts: (params = {}) => {
    const qs = new URLSearchParams(params).toString();
    return apiRequest(`/api/admin/products${qs ? "?" + qs : ""}`);
  },
  adminCreateProduct: (payload) => apiRequest("/api/admin/products", { method: "POST", body: JSON.stringify(payload) }),
  adminUpdateProduct: (id, payload) => apiRequest(`/api/admin/products/${id}`, { method: "PUT", body: JSON.stringify(payload) }),
  adminDeleteProduct: (id) => apiRequest(`/api/admin/products/${id}`, { method: "DELETE" }),
  adminListOrders: (statusFilter) => apiRequest(`/api/admin/orders${statusFilter ? "?status=" + encodeURIComponent(statusFilter) : ""}`),
  adminGetOrder: (orderId) => apiRequest(`/api/admin/orders/${orderId}`),
  adminUpdateOrderStatus: (orderId, status) =>
    apiRequest(`/api/admin/orders/${orderId}/status`, { method: "PUT", body: JSON.stringify({ order_status: status }) }),
};

function money(n) {
  return "₹" + Number(n).toLocaleString("en-IN", { maximumFractionDigits: 0 });
}

function showToast(message, type = "success") {
  let container = document.getElementById("toast-container");
  if (!container) {
    container = document.createElement("div");
    container.id = "toast-container";
    document.body.appendChild(container);
  }
  const toast = document.createElement("div");
  toast.className = `toast ${type === "error" ? "error" : ""}`;
  toast.textContent = message;
  container.appendChild(toast);
  setTimeout(() => toast.remove(), 3200);
}

function imgWithFallback(url, alt, cls = "") {
  const safeUrl = url || FALLBACK_IMAGE;
  return `<img src="${safeUrl}" alt="${alt.replace(/"/g, "&quot;")}" class="${cls}" loading="lazy" onerror="this.onerror=null;this.src='${FALLBACK_IMAGE}';">`;
}

function toggleMobileNav() {
  const nav = document.getElementById("navLinks");
  if (nav) nav.classList.toggle("mobile-open");
}

// ---------------- Navbar cart count + mobile toggle wiring ----------------
document.addEventListener("DOMContentLoaded", () => {
  updateCartCountBadge();
  const toggleBtn = document.getElementById("mobileToggle");
  if (toggleBtn) toggleBtn.addEventListener("click", toggleMobileNav);

  const searchForm = document.getElementById("navSearchForm");
  if (searchForm) {
    searchForm.addEventListener("submit", (e) => {
      e.preventDefault();
      const q = document.getElementById("navSearchInput").value.trim();
      window.location.href = `products.html?search=${encodeURIComponent(q)}`;
    });
  }
});
