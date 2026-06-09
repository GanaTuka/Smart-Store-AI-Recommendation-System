const homeProducts = document.getElementById('homeProducts');
const homeRecommendations = document.getElementById('homeRecommendations');
const homeStatus = document.getElementById('homeAiStatus');
const homeCustomerInput = document.getElementById('homeCustomerId');
const homeRecommendBtn = document.getElementById('homeRecommendBtn');

function displayCategory(category) {
    return category.split('_').filter(Boolean).map(word => word[0].toUpperCase() + word.slice(1)).join(' ');
}

function productTitle(category, suffix = 'Pick') {
    return `${displayCategory(category)} ${suffix}`;
}

function shortId(id) {
    return `${id.slice(0, 10)}...${id.slice(-4)}`;
}

function renderStoreCards(container, products, mode = 'product') {
    container.innerHTML = products.map(product => {
        const isAi = mode === 'ai';
        const fallback = product.model === 'popular_fallback';
        const badge = isAi ? (fallback ? 'Popular fallback' : `${Math.round(Number(product.score || 0) * 100)}% AI match`) : `${product.times_sold || product.popularity || 0} sales`;
        return `
            <article class="store-card">
                <div class="store-card-media">${displayCategory(product.category).slice(0, 2)}</div>
                <div class="store-card-body">
                    <span class="model-badge">${badge}</span>
                    <h3>${productTitle(product.category, isAi ? 'Recommendation' : 'Pick')}</h3>
                    <p class="product-id">Product ID: ${shortId(product.product_id)}</p>
                    ${isAi ? `<p>${product.explanation}</p>` : '<p>Popular item from real Olist purchase data.</p>'}
                    <div class="store-card-footer">
                        <strong>$${Number(product.avg_price || 0).toFixed(2)}</strong>
                        <small>${product.popularity || product.times_sold || 0} sales</small>
                    </div>
                </div>
            </article>
        `;
    }).join('');
}

async function loadPopularProducts() {
    try {
        const response = await fetch('/products');
        const products = await response.json();
        renderStoreCards(homeProducts, products.slice(0, 6));
    } catch (error) {
        homeProducts.innerHTML = '<p>Could not load product catalog.</p>';
    }
}

async function loadHomeRecommendations() {
    const customerId = homeCustomerInput.value.trim();
    if (!customerId) return;

    homeStatus.className = 'ai-status loading-status';
    homeStatus.innerHTML = '<strong>AI is working</strong><span>Building customer profile and ranking products.</span>';
    homeRecommendations.innerHTML = '<div class="loading-card">Loading AI picks...</div>';

    try {
        const response = await fetch(`/recommendations/${customerId}`);
        const products = await response.json();
        const fallback = products.every(product => product.model === 'popular_fallback');
        homeStatus.className = fallback ? 'ai-status fallback-status' : 'ai-status success-status';
        homeStatus.innerHTML = fallback
            ? '<strong>Popular fallback active</strong><span>The logged-in demo customer has limited matching history, so popular products are shown.</span>'
            : '<strong>AI recommendations active</strong><span>Products are ranked from the logged-in demo customer\'s purchase behavior.</span>';
        renderStoreCards(homeRecommendations, products, 'ai');
    } catch (error) {
        homeStatus.className = 'ai-status error-status';
        homeStatus.innerHTML = '<strong>AI unavailable</strong><span>Check MySQL and Flask logs.</span>';
        homeRecommendations.innerHTML = '';
    }
}

homeRecommendBtn.addEventListener('click', loadHomeRecommendations);
loadPopularProducts();
loadHomeRecommendations();
