const productGrid = document.getElementById('products');
const productSearch = document.getElementById('productSearch');
const productCount = document.getElementById('productCount');
const aiSearchAnswer = document.getElementById('aiSearchAnswer');
const askAiBtn = document.getElementById('askAiBtn');
const demoCustomerId = '06b8999e2fba1a1fbc88172c00ba8bc7';
let allProducts = [];

function displayCategory(category) {
    return category.split('_').filter(Boolean).map(word => word[0].toUpperCase() + word.slice(1)).join(' ');
}

function shortId(id) {
    return `${id.slice(0, 10)}...${id.slice(-4)}`;
}

function productVisual(category) {
    const label = displayCategory(category).slice(0, 2);
    return `
        <div class="product-visual" aria-label="${displayCategory(category)} product image">
            <span class="blob blob-main"></span>
            <span class="blob blob-side"></span>
            <span class="blob blob-leaf"></span>
            <em>${label}</em>
        </div>
    `;
}

function renderProducts(products, aiMode = false) {
    productCount.textContent = `${products.length} products shown`;
    productGrid.innerHTML = products.map(product => {
        const sales = product.times_sold || product.popularity || 0;
        return `
            <article class="store-card catalog-card">
                <div class="store-card-media">${productVisual(product.category)}</div>
                <div class="store-card-body">
                    <span class="model-badge">${aiMode ? 'Suggested for you' : `${sales} bought`}</span>
                    <h3>${displayCategory(product.category)} Pick</h3>
                    <p class="product-id">Catalog ref: ${shortId(product.product_id)}</p>
                    <p>${aiMode ? 'Chosen from your shopping request and customer profile.' : 'A frequently purchased item from this category.'}</p>
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
    aiSearchAnswer.className = `helper-answer ${type}`;
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
        showAiAnswer('loading-status', 'Tell me what you need', 'Ask for a product category, a budget, or a natural shopping question.');
        renderProducts(allProducts);
        return;
    }

    showAiAnswer('loading-status', 'Thinking about your request', 'I am checking matching products, prices, popularity, and your shopping profile.');

    try {
        const response = await fetch(`/products/search-ai?q=${encodeURIComponent(query)}&customer_id=${demoCustomerId}`);
        const result = await response.json();
        showAiAnswer('success-status', 'Here is my honest suggestion', result.answer);
        renderProducts(result.products, true);
    } catch (error) {
        showAiAnswer('error-status', 'I cannot answer right now', 'Please try again in a moment.');
    }
}

askAiBtn.addEventListener('click', () => {
    runAiSearch(productSearch.value.trim());
});

productSearch.addEventListener('keydown', event => {
    if (event.key === 'Enter' && !event.shiftKey) {
        event.preventDefault();
        runAiSearch(productSearch.value.trim());
    }
});

document.querySelectorAll('.helper-chip').forEach(chip => {
    chip.addEventListener('click', () => {
        productSearch.value = chip.dataset.query;
        runAiSearch(chip.dataset.query);
    });
});

loadProducts();
