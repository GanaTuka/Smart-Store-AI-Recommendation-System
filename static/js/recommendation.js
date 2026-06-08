const button = document.getElementById('recommendBtn');
const output = document.getElementById('recommendations');

async function loadRecommendations() {
    const userId = document.getElementById('userId').value || 1;
    output.innerHTML = '<p>Loading recommendations...</p>';
    const response = await fetch(`/recommendations/${userId}`);
    const products = await response.json();

    output.innerHTML = products.map(product => `
        <article class="card">
            <p class="eyebrow">${product.category}</p>
            <h3>${product.name}</h3>
            <p>Strong match for user #${userId}</p>
            <strong>$${Number(product.price).toFixed(2)}</strong>
        </article>
    `).join('') || '<p>No recommendations found.</p>';
}

button.addEventListener('click', loadRecommendations);
loadRecommendations();
