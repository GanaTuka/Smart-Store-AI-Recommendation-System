const button = document.getElementById('recommendBtn');
const output = document.getElementById('recommendations');

async function loadRecommendations() {
    const customerId = document.getElementById('customerId').value.trim();
    output.innerHTML = '<p>Loading recommendations...</p>';
    let products = [];

    try {
        const response = await fetch(`/recommendations/${customerId}`);
        products = await response.json();
    } catch (error) {
        output.innerHTML = '<p>Could not load recommendations. Check MySQL credentials and imported data.</p>';
        return;
    }

    output.innerHTML = products.map(product => `
        <article class="card">
            <p class="eyebrow">${product.category}</p>
            <h3>${product.product_id.slice(0, 12)}...</h3>
            <p>Recommended for customer ${customerId.slice(0, 10)}...</p>
            <p>AI similarity score: ${product.score}</p>
            <p>Store popularity: ${product.popularity} sales</p>
            <p>${product.explanation}</p>
            <strong>$${Number(product.avg_price || 0).toFixed(2)} avg</strong>
        </article>
    `).join('') || '<p>No recommendations found.</p>';
}

button.addEventListener('click', loadRecommendations);
loadRecommendations();
