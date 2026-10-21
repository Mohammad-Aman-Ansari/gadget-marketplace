let cart = JSON.parse(localStorage.getItem('gadgethub_cart')) || [];

const cartDrawer = document.getElementById('cart-drawer');
const cartItemsContainer = document.getElementById('cart-items');
const cartCount = document.getElementById('cart-count');
const cartTotal = document.getElementById('cart-total');

function saveAndRenderCart() {
    localStorage.setItem('gadgethub_cart', JSON.stringify(cart));
    const totalQty = cart.reduce((sum, item) => sum + item.qty, 0);
    const totalPrice = cart.reduce((sum, item) => sum + item.price * item.qty, 0);

    cartCount.textContent = totalQty;
    cartTotal.textContent = totalPrice.toLocaleString('en-IN', { minimumFractionDigits: 2 });

    if (cart.length === 0) {
        cartItemsContainer.innerHTML = '<p class="empty-cart">Your cart is empty.</p>';
        return;
    }

    cartItemsContainer.innerHTML = cart.map(item => `
        <div class="cart-item">
            <div>
                <h4>${item.title}</h4>
                <span class="cart-item-price">₹${item.price.toLocaleString('en-IN')} × ${item.qty}</span>
            </div>
            <div class="qty-controls">
                <button onclick="changeQty('${item.id}', -1)">−</button>
                <span>${item.qty}</span>
                <button onclick="changeQty('${item.id}', 1)">+</button>
            </div>
        </div>
    `).join('');
}

window.changeQty = function(id, delta) {
    const item = cart.find(g => g.id === id);
    if (!item) return;
    item.qty += delta;
    if (item.qty <= 0) {
        cart = cart.filter(g => g.id !== id);
    }
    saveAndRenderCart();
};

document.querySelectorAll('.add-to-cart-btn').forEach(btn => {
    btn.addEventListener('click', () => {
        const { id, title, price } = btn.dataset;
        const existing = cart.find(g => g.id === id);
        if (existing) {
            existing.qty += 1;
        } else {
            cart.push({ id, title, price: parseFloat(price), qty: 1 });
        }
        saveAndRenderCart();
        cartDrawer.classList.add('open');
    });
});

document.getElementById('cart-toggle').addEventListener('click', () => {
    cartDrawer.classList.toggle('open');
});

document.getElementById('close-cart').addEventListener('click', () => {
    cartDrawer.classList.remove('open');
});

document.getElementById('clear-cart').addEventListener('click', () => {
    cart = [];
    saveAndRenderCart();
});

saveAndRenderCart();
