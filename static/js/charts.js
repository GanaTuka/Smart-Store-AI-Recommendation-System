async function loadTopProducts() {
    const container = document.getElementById('topProducts');
    let products = [];

    try {
        const response = await fetch('/analytics/top-products');
        products = await response.json();
    } catch (error) {
        container.innerHTML = '<p>Could not load analytics. Check MySQL credentials and imported data.</p>';
        return;
    }
    const max = Math.max(...products.map(product => Number(product.units_sold)), 1);

    container.innerHTML = products.map(product => {
        const width = (Number(product.units_sold) / max) * 100;
        return `<div class="bar"><span style="width:${width}%">${product.category}: ${product.units_sold} sold, $${Number(product.revenue || 0).toFixed(2)}</span></div>`;
    }).join('') || '<p>No sales data yet.</p>';
}

loadTopProducts();
