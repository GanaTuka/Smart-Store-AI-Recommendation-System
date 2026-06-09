const currency = new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD', maximumFractionDigits: 0 });
const number = new Intl.NumberFormat('en-US');
const chartColors = ['#38bdf8', '#a7f3d0', '#fbbf24', '#fb7185', '#c084fc', '#60a5fa', '#34d399', '#f97316'];

async function fetchJson(path) {
    const response = await fetch(path);
    if (!response.ok) throw new Error(`Failed to load ${path}`);
    return response.json();
}

function renderSummary(summary) {
    const cards = [
        ['Total Revenue', currency.format(Number(summary.total_sales || 0)), 'From order item prices'],
        ['Orders', number.format(summary.total_orders || 0), 'Distinct Olist orders'],
        ['Customers', number.format(summary.total_customers || 0), 'Customers in database'],
        ['Products', number.format(summary.total_products || 0), 'Catalog size'],
        ['Avg Review', `${summary.average_review_score || 0}/5`, 'Customer satisfaction'],
    ];
    document.getElementById('summaryCards').innerHTML = cards.map(([label, value, caption]) => `
        <article class="kpi-card">
            <span>${label}</span>
            <strong>${value}</strong>
            <p>${caption}</p>
        </article>
    `).join('');
}

function barChart(id, labels, values, label) {
    new Chart(document.getElementById(id), {
        type: 'bar',
        data: { labels, datasets: [{ label, data: values, backgroundColor: chartColors }] },
        options: {
            responsive: true,
            plugins: { legend: { display: false } },
            scales: {
                x: { ticks: { color: '#9fb2c8' }, grid: { display: false } },
                y: { ticks: { color: '#9fb2c8' }, grid: { color: 'rgba(255,255,255,0.08)' } },
            },
        },
    });
}

function doughnutChart(id, labels, values) {
    new Chart(document.getElementById(id), {
        type: 'doughnut',
        data: { labels, datasets: [{ data: values, backgroundColor: chartColors }] },
        options: {
            responsive: true,
            plugins: { legend: { labels: { color: '#dbeafe' }, position: 'bottom' } },
        },
    });
}

function renderLeaderboard(id, rows, valueKey, valueLabel) {
    const max = Math.max(...rows.map(row => Number(row[valueKey])), 1);
    document.getElementById(id).innerHTML = rows.map(row => {
        const label = row.category || row.customer_state || row.product_id;
        const value = Number(row[valueKey]);
        const width = (value / max) * 100;
        return `
            <div class="leader-row">
                <div><strong>${label}</strong><span>${number.format(value)} ${valueLabel}</span></div>
                <div class="leader-track"><i style="width:${width}%"></i></div>
            </div>
        `;
    }).join('');
}

async function loadDashboard() {
    try {
        const [summary, categories, payments, reviews, products, states, business] = await Promise.all([
            fetchJson('/analytics/summary'),
            fetchJson('/analytics/top-categories'),
            fetchJson('/analytics/payment-breakdown'),
            fetchJson('/analytics/review-distribution'),
            fetchJson('/analytics/top-products'),
            fetchJson('/analytics/customer-states'),
            fetchJson('/analytics/business-recommendation'),
        ]);

        renderSummary(summary);
        document.getElementById('businessRecommendation').textContent = business.recommendation;
        document.getElementById('businessRecommendationSource').textContent = `Generated from ${business.source} using sales, category, payment, and review analytics.`;
        barChart('categoryChart', categories.map(row => row.category), categories.map(row => Number(row.revenue)), 'Revenue');
        doughnutChart('paymentChart', payments.map(row => row.payment_type), payments.map(row => Number(row.payment_value)));
        doughnutChart('reviewChart', reviews.map(row => `${row.review_score} stars`), reviews.map(row => Number(row.review_count)));
        renderLeaderboard('topProducts', products, 'units_sold', 'sold');
        renderLeaderboard('stateList', states, 'orders', 'orders');
    } catch (error) {
        document.querySelector('.admin-page').insertAdjacentHTML('afterbegin', '<section class="ai-status error-status"><strong>Analytics unavailable</strong><span>Check MySQL credentials and imported data.</span></section>');
    }
}

loadDashboard();
