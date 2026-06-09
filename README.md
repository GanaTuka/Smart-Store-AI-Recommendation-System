# Smart-Store-AI-Recommendation-System

Hackathon-ready smart store recommendation system using one Flask app, one MySQL database, and one local open-source AI recommendation module.

## Core API Contract

- `GET /products`
- `GET /recommendations/<customer_id>`
- `GET /analytics/top-products`

## Pages

- `/login`
- `/product-list`
- `/recommendations`
- `/admin`

## Project Structure

```text
Smart-Store-AI-Recommendation-System/
├── app.py
├── ai/
├── analytics/
├── database/
├── dataset/
├── docs/
├── routes/
├── static/
└── templates/
```

## Quick Start

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
mysql -u root -p < database/schema.sql
python -m database.import_data
python app.py
```

Open `http://127.0.0.1:5000`.

Use a real `customer_id` from `dataset/olist_customers_dataset.csv` on the recommendations page. Example:

```text
06b8999e2fba1a1fbc88172c00ba8bc7
```

## Team Split

- Database: `database/`, `dataset/`
- Backend: `app.py`, `routes/`
- Frontend: `templates/`, `static/`
- AI: `ai/`
- Analytics and docs: `analytics/`, `docs/`

## Recommendation Logic

The recommendation module uses a local `scikit-learn` content-based model. It builds product vectors from category text, average price, popularity, and product dimensions, then ranks products by cosine similarity to the customer's purchase history. No external API key is required.
