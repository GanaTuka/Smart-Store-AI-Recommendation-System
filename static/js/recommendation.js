const button = document.getElementById('recommendBtn');
const output = document.getElementById('recommendations');
const statusBox = document.getElementById('aiStatus');
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

function setStatus(products) {
    if (!products.length) {
        statusBox.className = 'ai-status error-status';
        statusBox.innerHTML = '<strong>No recommendations found</strong><span>We could not find enough shopping history for this profile.</span>';
        return;
    }

    const usesFallback = products.every(product => product.model === 'popular_fallback');
    const explanationSource = products[0].explanation_source || 'template_fallback';

    if (usesFallback) {
        statusBox.className = 'ai-status fallback-status';
        statusBox.innerHTML = `
            <strong>Popular picks selected</strong>
            <span>Your profile has limited matching history, so these recommendations are based on store-wide performance.</span>
            <small>Explanation source: ${explanationSource}</small>
        `;
        return;
    }

    statusBox.className = 'ai-status success-status';
    statusBox.innerHTML = `
        <strong>Personalized recommendations active</strong>
        <span>These products are ranked from your purchase behavior using content-based AI similarity.</span>
        <small>Explanation source: ${explanationSource}</small>
    `;
}

function renderLoading() {
    output.innerHTML = `
        <div class="loading-card">Building your shopping profile...</div>
        <div class="loading-card">Ranking products from purchase history...</div>
        <div class="loading-card">Preparing recommendation reasons...</div>
    `;
    statusBox.className = 'ai-status loading-status';
    statusBox.innerHTML = '<strong>AI is working</strong><span>Reading your purchase history and ranking products from live store data.</span>';
}

async function loadRecommendations() {
    const customerInput = document.getElementById('customerId');
    const customerId = customerInput.value.trim() || demoCustomerId;
    renderLoading();

    let products = [];

    try {
        const response = await fetch(`/recommendations/${customerId}`);
        if (!response.ok) throw new Error('Recommendation request failed');
        products = await response.json();
    } catch (error) {
        statusBox.className = 'ai-status error-status';
        statusBox.innerHTML = '<strong>Recommendations unavailable</strong><span>Please check MySQL, imported data, and the Flask server logs.</span>';
        output.innerHTML = '';
        return;
    }

    setStatus(products);

    output.innerHTML = products.map((product, index) => {
        const isFallback = product.model === 'popular_fallback';
        const title = titleFromCategory(product.category, isFallback);
        const scorePercent = Math.round(Number(product.score || 0) * 100);
        const badge = isFallback ? 'Popular pick' : `${scorePercent}% AI match`;
        const modelText = isFallback
            ? 'Selected from high-performing store products'
            : 'Matched from your purchase behavior';

        return `
            <article class="recommendation-card ${isFallback ? 'fallback-card' : ''}">
                <div class="card-topline">
                    <span class="rank-badge">#${index + 1}</span>
                    <span class="model-badge">${badge}</span>
                </div>
                <p class="eyebrow">${product.category.replaceAll('_', ' ')}</p>
                <h3>${title}</h3>
                <p class="product-id">Catalog reference: ${shortProductId(product.product_id)}</p>
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

button.addEventListener('click', loadRecommendations);
loadRecommendations();
