const button = document.getElementById('recommendBtn');
const output = document.getElementById('recommendations');
const statusBox = document.getElementById('aiStatus');
const demoButton = document.getElementById('demoCustomer');
const demoCustomerId = '06b8999e2fba1a1fbc88172c00ba8bc7';

function titleFromCategory(category, isFallback) {
    const label = category
        .split('_')
        .filter(Boolean)
        .map(word => word.charAt(0).toUpperCase() + word.slice(1))
        .join(' ');

    return isFallback ? `Popular ${label} Pick` : `${label} Recommendation`;
}

function shortProductId(productId) {
    return `${productId.slice(0, 10)}...${productId.slice(-4)}`;
}

function setStatus(products, customerId) {
    if (!products.length) {
        statusBox.className = 'ai-status error-status';
        statusBox.innerHTML = '<strong>No recommendations found.</strong><span>Check that the customer ID exists in the Olist dataset.</span>';
        return;
    }

    const fallbackCount = products.filter(product => product.model === 'popular_fallback').length;
    const usesFallback = fallbackCount === products.length;
    const explanationSource = products[0].explanation_source || 'template_fallback';

    if (usesFallback) {
        statusBox.className = 'ai-status fallback-status';
        statusBox.innerHTML = `
            <strong>Popular fallback active</strong>
            <span>Customer ${customerId.slice(0, 10)}... has no usable purchase-history match in the AI catalog, so we are showing strong store-wide picks.</span>
            <small>Explanation source: ${explanationSource}</small>
        `;
        return;
    }

    statusBox.className = 'ai-status success-status';
    statusBox.innerHTML = `
        <strong>AI recommendation engine active</strong>
        <span>Products are ranked from this customer's purchase history using content-based ML similarity.</span>
        <small>Explanation source: ${explanationSource}</small>
    `;
}

async function loadRecommendations() {
    const customerId = document.getElementById('customerId').value.trim();
    output.innerHTML = '<div class="loading-card">Building customer profile and ranking products...</div>';
    statusBox.className = 'ai-status loading-status';
    statusBox.innerHTML = '<strong>AI is working</strong><span>Reading MySQL purchase history, ranking products, and preparing explanations.</span>';

    if (!customerId) {
        statusBox.className = 'ai-status error-status';
        statusBox.innerHTML = '<strong>Customer ID required</strong><span>Paste an Olist customer ID to generate recommendations.</span>';
        output.innerHTML = '';
        return;
    }

    let products = [];

    try {
        const response = await fetch(`/recommendations/${customerId}`);
        if (!response.ok) throw new Error('Recommendation request failed');
        products = await response.json();
    } catch (error) {
        statusBox.className = 'ai-status error-status';
        statusBox.innerHTML = '<strong>Recommendation engine unavailable</strong><span>Check MySQL, imported data, and the Flask server logs.</span>';
        output.innerHTML = '';
        return;
    }

    setStatus(products, customerId);

    output.innerHTML = products.map((product, index) => {
        const isFallback = product.model === 'popular_fallback';
        const title = titleFromCategory(product.category, isFallback);
        const scorePercent = Math.round(Number(product.score || 0) * 100);
        const badge = isFallback ? 'Popular fallback' : `${scorePercent}% AI match`;
        const modelText = isFallback
            ? 'Selected from popular store-wide products'
            : 'Matched from customer purchase behavior';

        return `
            <article class="recommendation-card ${isFallback ? 'fallback-card' : ''}">
                <div class="card-topline">
                    <span class="rank-badge">#${index + 1}</span>
                    <span class="model-badge">${badge}</span>
                </div>
                <p class="eyebrow">${product.category.replaceAll('_', ' ')}</p>
                <h3>${title}</h3>
                <p class="product-id">Product ID: ${shortProductId(product.product_id)}</p>
                <div class="metric-row">
                    <div><span>${product.popularity}</span><small>sales</small></div>
                    <div><span>$${Number(product.avg_price || 0).toFixed(2)}</span><small>avg price</small></div>
                </div>
                <div class="why-box">
                    <strong>Why this pick?</strong>
                    <p>${product.explanation}</p>
                </div>
                <p class="model-note">${modelText}</p>
            </article>
        `;
    }).join('') || '<p>No recommendations found.</p>';
}

demoButton.addEventListener('click', () => {
    document.getElementById('customerId').value = demoCustomerId;
    loadRecommendations();
});

button.addEventListener('click', loadRecommendations);
loadRecommendations();
