async function loadTopProducts() {
    const container = document.getElementById('topProducts');
    const response = await fetch('/analytics/top-products');
    const products = await response.json();
    const max = Math.max(...products.map(product => Number(product.units_sold)), 1);

    container.innerHTML = products.map(product => {
        const width = (Number(product.units_sold) / max) * 100;
        return `<div class="bar"><span style="width:${width}%">${product.name}: ${product.units_sold}</span></div>`;
    }).join('') || '<p>No sales data yet.</p>';
}

loadTopProducts();
