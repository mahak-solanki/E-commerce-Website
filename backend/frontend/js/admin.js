function requireAdminAuth() {
  const token = localStorage.getItem("abb_admin_token");
  if (!token) {
    window.location.href = "../login.html";
    return false;
  }
  return true;
}

function adminLogout() {
  localStorage.removeItem("abb_admin_token");
  window.location.href = "../login.html";
}

function renderAdminSidebar(active) {
  const item = (page, href, label) =>
    `<a href="${href}" class="${active === page ? "active" : ""}">${label}</a>`;
  return `
  <div class="admin-sidebar">
    <div class="brand">🕉️ Annapurna Admin</div>
    ${item("dashboard", "dashboard.html", "📊 Dashboard")}
    ${item("products", "products.html", "🛍️ Products")}
    ${item("orders", "orders.html", "📦 Orders")}
    <a href="../index.html">🏠 View Website</a>
    <a href="#" onclick="adminLogout(); return false;">🚪 Logout</a>
  </div>`;
}

async function handleAdminApiError(e) {
  if (e.status === 401) {
    showToast("Session expired. Please login again.", "error");
    setTimeout(() => { localStorage.removeItem("abb_admin_token"); window.location.href = "../login.html"; }, 1200);
    return true;
  }
  return false;
}
