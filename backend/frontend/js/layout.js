function renderNavbar(activePage = "") {
  const nav = (page, href, label) =>
    `<a href="${href}" class="${activePage === page ? "active" : ""}">${label}</a>`;

  return `
  <div class="announce-bar">✨ Home Delivery Available Across India | Cash on Delivery | Certified Rudraksha ✨</div>
  <nav class="navbar">
    <div class="navbar-inner">
      <a href="index.html" class="brand"><span class="om">🕉️</span> Annapurna Bhakti Bhandar</a>
      <button id="mobileToggle" class="mobile-toggle" aria-label="Menu">☰</button>
      <div class="nav-links" id="navLinks">
        ${nav("home", "index.html", "Home")}
        ${nav("girls", "products.html?category=girls-collection", "Girls Collection")}
        ${nav("rudraksha", "products.html?category=certified-rudraksha", "Rudraksha")}
        ${nav("rashi", "products.html?category=rashi-ratna-bracelets", "Rashi Ratna Bracelets")}
      </div>
      <div class="nav-actions">
        <form id="navSearchForm" class="search-box">
          <input id="navSearchInput" type="text" placeholder="Search products..." />
          <button type="submit" style="background:none;border:none;cursor:pointer;">🔍</button>
        </form>
        <a href="cart.html" class="icon-btn" title="Cart">🛒<span id="cartCount" class="cart-count">0</span></a>
        <a href="login.html" class="icon-btn" title="Admin Login">👤</a>
      </div>
    </div>
  </nav>`;
}

function renderFooter() {
  return `
  <footer>
    <div class="container footer-grid">
      <div class="footer-brand">
        <h4>Annapurna Bhakti Bhandar</h4>
        <p>Your trusted destination for beautiful women's accessories, certified Rudraksha, and
        Rashi-based Ratna gemstone bracelets — delivered to your doorstep across India.</p>
        <div class="social-row">
          <a href="#" title="Facebook">f</a>
          <a href="#" title="Instagram">ig</a>
          <a href="#" title="YouTube">yt</a>
        </div>
      </div>
      <div>
        <h4>Quick Links</h4>
        <ul>
          <li><a href="index.html">Home</a></li>
          <li><a href="products.html?category=girls-collection">Girls Collection</a></li>
          <li><a href="products.html?category=certified-rudraksha">Rudraksha</a></li>
          <li><a href="products.html?category=rashi-ratna-bracelets">Rashi Bracelets</a></li>
        </ul>
      </div>
      <div>
        <h4>Customer Support</h4>
        <ul>
          <li>📞 <span id="footerPhone">CHANGE_ME</span></li>
          <li>✉️ <span id="footerEmail">CHANGE_ME</span></li>
          <li>💬 <a href="#" id="footerWhatsapp">Chat on WhatsApp</a></li>
        </ul>
      </div>
      <div>
        <h4>Address</h4>
        <ul>
          <li id="footerAddress">CHANGE_ME</li>
        </ul>
      </div>
    </div>
    <div class="footer-bottom">
      © <span id="footerYear"></span> Annapurna Bhakti Bhandar. All rights reserved. | Demo storefront built for demonstration purposes.
    </div>
  </footer>
  <a href="#" id="whatsappFloat" class="whatsapp-float" title="Chat on WhatsApp">💬</a>
  `;
}

async function mountLayout(activePage) {
  const navMount = document.getElementById("navbar-mount");
  const footerMount = document.getElementById("footer-mount");
  if (navMount) navMount.innerHTML = renderNavbar(activePage);
  if (footerMount) footerMount.innerHTML = renderFooter();

  document.dispatchEvent(new Event("DOMContentLoaded-layout"));
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

  const yearEl = document.getElementById("footerYear");
  if (yearEl) yearEl.textContent = new Date().getFullYear();

  try {
    const cfg = await api.getConfig();
    const phone = document.getElementById("footerPhone");
    const email = document.getElementById("footerEmail");
    const addr = document.getElementById("footerAddress");
    const wa = document.getElementById("footerWhatsapp");
    const waFloat = document.getElementById("whatsappFloat");
    if (phone) phone.textContent = cfg.shop_phone;
    if (email) email.textContent = cfg.shop_email;
    if (addr) addr.textContent = cfg.shop_address;
    const waNumber = cfg.whatsapp_number && cfg.whatsapp_number !== "CHANGE_ME" ? cfg.whatsapp_number : null;
    const waLink = waNumber
      ? `https://wa.me/${waNumber}?text=${encodeURIComponent("Hi, I need help with a product from Annapurna Bhakti Bhandar.")}`
      : "#";
    if (wa) wa.href = waLink;
    if (waFloat) {
      waFloat.href = waLink;
      if (!waNumber) {
        waFloat.addEventListener("click", (e) => {
          e.preventDefault();
          showToast("WhatsApp number not configured yet. Set WHATSAPP_NUMBER in .env", "error");
        });
      }
    }
  } catch (e) {
    console.warn("Could not load shop config", e);
  }
}
