# API Contract

## GET /products

Returns popular Olist products with category, average price, and sales count.

Example fields:

```json
{
  "product_id": "...",
  "category": "housewares",
  "avg_price": "45.90",
  "times_sold": 12
}
```

## GET /recommendations/&lt;customer_id&gt;

Returns recommended Olist products for one customer based on previously purchased categories.

Example fields:

```json
{
  "product_id": "...",
  "category": "health_beauty",
  "avg_price": "39.90",
  "score": 20
}
```

## GET /analytics/top-products

Returns top-selling Olist products with revenue.
