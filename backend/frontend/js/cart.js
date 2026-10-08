// ---------------------------------------------------------------
// Guest cart, stored in localStorage as an array of
// { product_id, name, image, price, stock, quantity }
// ---------------------------------------------------------------
const CART_KEY = "abb_cart";

function getCart() {
  try {
    return JSON.parse(localStorage.getItem(CART_KEY)) || [];
  } catch (e) {
    return [];
  }
}

function saveCart(cart) {
  localStorage.setItem(CART_KEY, JSON.stringify(cart));
  updateCartCountBadge();
}

function cartCount() {
  return getCart().reduce((sum, i) => sum + i.quantity, 0);
}

function updateCartCountBadge() {
  const badge = document.getElementById("cartCount");
  if (badge) {
    const count = cartCount();
    badge.textContent = count;
    badge.style.display = count > 0 ? "flex" : "none";
  }
}

function addToCart(product, qty = 1) {
  const cart = getCart();
  const existing = cart.find((i) => i.product_id === product.id);
  const unitPrice = product.discount_price || product.price;
  const maxQty = product.stock_quantity;

  if (existing) {
    existing.quantity = Math.min(existing.quantity + qty, maxQty);
  } else {
    cart.push({
      product_id: product.id,
      name: product.name,
      image: product.image_url,
      price: unitPrice,
      stock: maxQty,
      quantity: Math.min(qty, maxQty),
    });
  }
  saveCart(cart);
  showToast(`${product.name} added to cart`);
}

function removeFromCart(productId) {
  const cart = getCart().filter((i) => i.product_id !== productId);
  saveCart(cart);
}

function setCartQuantity(productId, qty) {
  const cart = getCart();
  const item = cart.find((i) => i.product_id === productId);
  if (!item) return;
  if (qty <= 0) {
    return removeFromCart(productId);
  }
  item.quantity = Math.min(qty, item.stock);
  saveCart(cart);
}

function clearCart() {
  saveCart([]);
}

function cartSubtotal() {
  return getCart().reduce((sum, i) => sum + i.price * i.quantity, 0);
}
