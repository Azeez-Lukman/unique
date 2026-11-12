# Unique Property & Construction Company — Web Application

A modern, responsive, full-stack website and enquiry management system for **Unique Property & Construction Company**, built with Python, Django, Tailwind CSS v4, and PostgreSQL.

> **“If you can dream it, we can build it.”**

---

## 1. Approved Technology Stack

The project adheres strictly to the approved architectural stack:

- **Backend:** Python & Django 6.1 (Routing, Models, Forms, Business Logic, Administration)
- **Frontend Rendering:** Django Templates & Semantic HTML5
- **Styling:** Tailwind CSS v4 (pure CSS-first compilation via `@tailwindcss/cli`, no v3 legacy configs)
- **Frontend Interactivity:** Vanilla JavaScript (ES6+) — zero heavy frontend SPA frameworks
- **Database:** PostgreSQL (Primary Relational Database via `psycopg 3` and Django ORM)
- **Tooling:** Python `venv`, Node.js & npm (for Tailwind v4 CLI only), Git version control
- **Design & Icons:** Lucide Icons, Google Fonts (`Outfit`, `Playfair Display`, `Plus Jakarta Sans`)

---

## 2. Project Directory Structure

```
unique/
├── .env                  # Local environment configuration (ignored by Git)
├── .env.example          # Template for environment variables
├── .gitignore            # Excludes venv, node_modules, secrets, sqlite, media
├── manage.py             # Django CLI management script
├── package.json          # Node.js scripts for Tailwind CSS v4 CLI
├── requirements.txt      # Pinned Python dependencies
├── README.md             # Complete technical and local development guide
├── project_status.md     # Phase-by-phase project progress log
├── TODO.md               # Master project milestone checklist
├── RECOMMENDATION.md     # Brand, UX, and technical architectural record
│
├── config/               # Django Project Configuration Root
│   ├── settings.py       # Environment-based settings (PostgreSQL/SQLite, static, auth)
│   ├── urls.py           # Master URL routing (includes sitemap.xml & robots.txt)
│   ├── wsgi.py           # WSGI entry point
│   └── asgi.py           # ASGI entry point
│
├── core/                 # Core Business Application
│   ├── admin.py          # Django Admin interface for Enquiries and Properties
│   ├── forms.py          # Django Forms with server-side validation & styling
│   ├── models.py         # Database schema (Enquiry, Property)
│   ├── sitemaps.py       # Dynamic XML Sitemap generator
│   ├── tests.py          # Automated test suite (12 tests)
│   ├── urls.py           # Application routes (home, about, services, contact)
│   └── views.py          # View logic, form processing, notification dispatch
│
├── static/               # Static Assets
│   ├── css/
│   │   ├── input.css     # Tailwind v4 source with @theme brand tokens
│   │   └── output.css    # Compiled production stylesheet
│   ├── images/           # Brand logo and curated architectural photography
│   └── js/
│       └── main.js       # Vanilla JS (mobile navigation, alerts, UI helpers)
│
└── templates/            # Django Templates Hierarchy
    ├── base.html         # Global base layout (header, nav, footer, Schema.org)
    └── core/
        ├── index.html         # Homepage (Hero, dual divisions, 4-step process, enquiry)
        ├── about.html         # About Us (Philosophy, values, standards)
        ├── construction.html  # Residential & Commercial construction
        ├── real_estate.html   # Property management & leasing services
        ├── properties.html    # Property showcase & acquisition sourcing desk
        └── contact.html       # Interactive enquiry form, WhatsApp, direct telephone
```

---

## 3. Local Development Setup Guide

### Step 1: Clone & Navigate
```bash
git clone <repository-url>
cd unique
```

### Step 2: Python Virtual Environment
Activate the existing virtual environment or create a new one:
```powershell
# Windows PowerShell
.\.venv\Scripts\Activate.ps1

# Or recreate:
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Install Python dependencies:
```bash
pip install -r requirements.txt
```

### Step 3: Configure Environment Variables
Copy `.env.example` to `.env`:
```powershell
Copy-Item .env.example .env
```
Ensure your `.env` contains:
- `DEBUG=True`
- `SECRET_KEY=<your-development-secret-key>`
- `DB_ENGINE=django.db.backends.postgresql` (or `sqlite3` for quick local prototyping)
- `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST`, `DB_PORT`

### Step 4: PostgreSQL Setup
Create your local PostgreSQL database:
```sql
CREATE DATABASE unique_db;
CREATE USER postgres WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE unique_db TO postgres;
```
*(If local PostgreSQL is not currently running, set `DB_ENGINE=django.db.backends.sqlite3` in `.env` for zero-friction local execution).*

Apply migrations:
```bash
python manage.py migrate
```

### Step 5: Tailwind CSS v4 Tooling
Install Node.js dependencies:
```bash
npm install
```

Build the stylesheet once:
```bash
npm run build:css
```

Or run the watcher during active template editing:
```bash
npm run watch:css
```

### Step 6: Create an Administrator
```bash
python manage.py createsuperuser
```

### Step 7: Run the Development Server
```bash
python manage.py runserver
```
Visit `http://127.0.0.1:8000/` in your browser.  
Access the admin portal at `http://127.0.0.1:8000/admin/`.

---

## 4. Running the Automated Test Suite

Run the full Django test suite:
```bash
python manage.py test core
```
*Current test suite status: 12 tests passing, 0 issues identified.*

---

## 5. Technology Governance & Rules

As specified in the project governance:
- **No React, Next.js, Vue, or Angular.**
- **No Node.js backend frameworks.**
- All dynamic pages are rendered server-side via **Django Templates**.
- All styles are compiled via **Tailwind CSS v4** without mixing v3 configurations.
- Client submissions are handled securely with **Django Forms** and CSRF protection.
