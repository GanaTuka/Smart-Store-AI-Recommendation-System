const productGrid = document.getElementById('products');
const productSearch = document.getElementById('productSearch');
const productCount = document.getElementById('productCount');
let allProducts = [];

function displayCategory(category) {
    return category.split('_').filter(Boolean).map(word => word[0].toUpperCase() + word.slice(1)).join(' ');
}

function shortId(id) {
    return `${id.slice(0, 10)}...${id.slice(-4)}`;
}

function renderProducts(products) {
    productCount.textContent = `${products.length} products shown`;
    productGrid.innerHTML = products.map(product => `
        <article class="store-card catalog-card">
            <div class="store-card-media">${displayCategory(product.category).slice(0, 2)}</div>
            <div class="store-card-body">
                <span class="model-badge">${product.times_sold || 0} sales</span>
                <h3>${displayCategory(product.category)} Pick</h3>
                <p class="product-id">Product ID: ${shortId(product.product_id)}</p>
                <p>Popular product category from Olist order history.</p>
                <div class="store-card-footer">
                    <strong>$${Number(product.avg_price || 0).toFixed(2)}</strong>
                    <small>avg price</small>
                </div>
            </div>
        </article>
    `).join('') || '<p>No products match your search.</p>';
}

async function loadProducts() {
    try {
        const response = await fetch('/products');
        allProducts = await response.json();
        renderProducts(allProducts);
    } catch (error) {
        productGrid.innerHTML = '<p>Could not load products. Check MySQL credentials and imported data.</p>';
        productCount.textContent = 'Catalog unavailable';
    }
}

productSearch.addEventListener('input', () => {
    const query = productSearch.value.toLowerCase().trim();
    const filtered = allProducts.filter(product => product.category.toLowerCase().includes(query));
    renderProducts(filtered);
});

loadProducts();
