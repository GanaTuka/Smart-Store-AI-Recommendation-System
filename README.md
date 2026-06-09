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

## Database Setup Checklist

After pulling the latest code, every teammate must create their own local `.env` and local MySQL database. The database data is not stored in GitHub.

```bash
cp .env.example .env
```

Edit `.env` for that machine's MySQL account:

```env
MYSQL_HOST=localhost
MYSQL_USER=root
MYSQL_PASSWORD=your_mysql_password
MYSQL_DATABASE=smart_store
```

Then run:

```bash
mysql -u root -p < database/schema.sql
python -m database.import_data
python -m database.check_connection
```

If `python app.py` cannot connect to MySQL, run the diagnostic first:

```bash
python -m database.check_connection
```

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

The recommendation module uses a local `scikit-learn` content-based model. It builds product vectors from category text, average price, popularity, and product dimensions, then ranks products by cosine similarity to the customer's purchase history.

The explanation layer uses Ollama with a local model such as `gemma3:1b` or `llama3.2:3b`. If Ollama is not running, the app automatically falls back to a rule-based explanation, so the demo still works.

## Optional Ollama Setup

Install and run Ollama, then pull a small local model:

```bash
ollama pull gemma3:1b
```

Use these `.env` values:

```env
OLLAMA_ENABLED=true
OLLAMA_URL=http://localhost:11434/api/generate
OLLAMA_MODEL=gemma3:1b
OLLAMA_TIMEOUT=8
```

Alternative model:

```env
OLLAMA_MODEL=llama3.2:3b
```

If Ollama is unavailable, no error is shown to the user; the fallback explanation is used.
