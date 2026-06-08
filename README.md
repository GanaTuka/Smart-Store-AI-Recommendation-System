# Smart-Store-AI-Recommendation-System

Hackathon-ready smart store recommendation system using one Flask app, one MySQL database, and one AI recommendation module.

## Core API Contract

- `GET /products`
- `GET /recommendations/<user_id>`
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
mysql -u root -p < database/seed_data.sql
python app.py
```

Open `http://127.0.0.1:5000`.

## Team Split

- Database: `database/`, `dataset/`
- Backend: `app.py`, `routes/`
- Frontend: `templates/`, `static/`
- AI: `ai/`
- Analytics and docs: `analytics/`, `docs/`

## Recommendation Logic

The first version recommends highly rated products from categories the user already bought from. If a user has no order history, it falls back to top-rated products.
