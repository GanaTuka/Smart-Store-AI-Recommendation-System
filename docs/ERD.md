# ERD

Olist database tables used by the demo:

```text
customers 1--* orders 1--* order_items *--1 products
                              |
                              *--1 sellers

orders 1--* payments
orders 1--* reviews
products *--1 category_translation
```

Core recommendation path:

```text
customers -> orders -> order_items -> products -> category_translation
```
