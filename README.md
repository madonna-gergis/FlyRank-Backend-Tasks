# 🚀 FlyRank Backend AI Engineering Assignments

Welcome to my repository containing backend assignments and projects completed during the **FlyRank AI Engineering Internship**.

---

## 📁 Repository Structure

```text
FlyRank-Backend-Tasks/
├── todo-api/          # BE-04: FastAPI & Supabase Authentication System
├── polite-scraper/    # BE-05: Web Scraper for 60 Books (Clean JSON Output)
└── README.md          # Overview & Documentation
```

---

## 🛠️ Included Projects

### 1. 🔐 Todo & Auth API (`todo-api/`)
* **Framework:** FastAPI
* **Database & Auth:** Supabase
* **Features:**
  * User Registration (`/auth/signup`)
  * User Authentication (`/auth/login`)
  * Interactive API documentation via Swagger UI (`/docs`)

---

### 2. 🕷️ The Polite Scraper (`polite-scraper/`)
* **Language & Libraries:** Python, `requests`, `beautifulsoup4`
* **Features:**
  * Scrapes **60 books** across 3 pages from Books to Scrape.
  * Cleans messy HTML text (converts prices like `£51.77` to numeric floats).
  * Extracts book titles, prices, stock availability, and rating scores.
  * Respects server resources using custom `User-Agent` headers and `1-second` rate limiting delays.
  * Outputs validated and structured data directly to `books.json`.

---

## 💻 How to Run Locally

### Polite Scraper
```bash
cd polite-scraper
pip install requests beautifulsoup4
python scraper.py
```

### Auth & Todo API
```bash
cd todo-api
pip install fastapi uvicorn supabase python-dotenv pydantic
python -m uvicorn main:app --reload
```