const productGrid = document.getElementById('products');
const productSearch = document.getElementById('productSearch');
const productCount = document.getElementById('productCount');
const aiSearchAnswer = document.getElementById('aiSearchAnswer');
const demoCustomerId = '06b8999e2fba1a1fbc88172c00ba8bc7';
let allProducts = [];
let searchTimer = null;

function displayCategory(category) {
    return category.split('_').filter(Boolean).map(word => word[0].toUpperCase() + word.slice(1)).join(' ');
}

function shortId(id) {
    return `${id.slice(0, 10)}...${id.slice(-4)}`;
}

function renderProducts(products, aiMode = false) {
    productCount.textContent = `${products.length} products shown`;
    productGrid.innerHTML = products.map(product => {
        const sales = product.times_sold || product.popularity || 0;
        return `
            <article class="store-card catalog-card">
                <div class="store-card-media">${displayCategory(product.category).slice(0, 2)}</div>
                <div class="store-card-body">
                    <span class="model-badge">${aiMode ? 'AI database match' : `${sales} sales`}</span>
                    <h3>${displayCategory(product.category)} Pick</h3>
                    <p class="product-id">Product ID: ${shortId(product.product_id)}</p>
                    <p>${aiMode ? 'Selected from your AI search using Olist sales data.' : 'Popular item from real Olist purchase data.'}</p>
                    <div class="store-card-footer">
                        <strong>$${Number(product.avg_price || 0).toFixed(2)}</strong>
                        <small>${sales} sales</small>
                    </div>
                </div>
            </article>
        `;
    }).join('') || '<p>No products match your search.</p>';
}

function showAiAnswer(type, title, message) {
    aiSearchAnswer.className = `ai-status ${type}`;
    aiSearchAnswer.innerHTML = `<strong>${title}</strong><span>${message}</span>`;
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

async function runAiSearch(query) {
    if (!query) {
        showAiAnswer('loading-status', 'AI shopping assistant ready', 'Type a product idea, category, or budget to search the database.');
        renderProducts(allProducts);
        return;
    }

    showAiAnswer('loading-status', 'AI is searching the catalog', 'Reading MySQL product data and generating a grounded shopping answer.');

    try {
        const response = await fetch(`/products/search-ai?q=${encodeURIComponent(query)}&customer_id=${demoCustomerId}`);
        const result = await response.json();
        showAiAnswer('success-status', 'AI shopping answer', result.answer);
        renderProducts(result.products, true);
    } catch (error) {
        showAiAnswer('error-status', 'AI search unavailable', 'Check MySQL, Flask logs, and the local Ollama server.');
    }
}

productSearch.addEventListener('input', () => {
    clearTimeout(searchTimer);
    const query = productSearch.value.trim();
    searchTimer = setTimeout(() => runAiSearch(query), 550);
});

loadProducts();
