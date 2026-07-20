# Meridian — Hospital Management System

A Flask + MySQL hospital admin panel: patients, doctors, appointments,
billing, and a Pandas/Matplotlib analytics dashboard.

> **Note:** This is a dynamic Flask app that needs Python and MySQL.
> It **cannot** run on static hosts like Netlify or GitHub Pages —
> use a Python host such as **Render**, **Railway**, or **PythonAnywhere**.

## Tech stack
- Flask 3 (Python 3.12)
- MySQL 8
- Pandas + Matplotlib (analytics/charts, `Agg` headless backend)
- Gunicorn (production server)

## Local setup

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Create the database and seed data
mysql -u root -p < schema.sql
mysql -u root -p hospital_db < seed_more.sql
mysql -u root -p hospital_db < seed_more2.sql
mysql -u root -p hospital_db < seed_bills.sql

# 3. Configure DB access (defaults in config.py, override via env vars)
export HMS_DB_HOST=localhost
export HMS_DB_USER=root
export HMS_DB_PASSWORD=yourpassword
export HMS_DB_NAME=hospital_db

# 4. Run
python app.py
# open http://localhost:5000
```

## Environment variables

| Variable            | Default        | Description              |
|---------------------|----------------|--------------------------|
| `HMS_DB_HOST`       | `localhost`    | MySQL host               |
| `HMS_DB_PORT`       | `3306`         | MySQL port               |
| `HMS_DB_USER`       | `root`         | MySQL user               |
| `HMS_DB_PASSWORD`   | `rootpass`     | MySQL password           |
| `HMS_DB_NAME`       | `hospital_db`  | Database name            |
| `HMS_SECRET_KEY`    | dev key        | Flask session secret     |

## Deploy to Render (free)

Render runs the Flask app, but its free managed DB is PostgreSQL — this app
needs **MySQL**, so provision a free MySQL elsewhere (e.g. **Railway**,
**Aiven**, or **Clever Cloud**) and point the app at it.

1. Create a free MySQL database on Railway/Aiven and note its
   host, port, user, password, and database name.
2. Load the schema + seed data into that MySQL instance:
   ```bash
   mysql -h <host> -P <port> -u <user> -p <dbname> < schema.sql
   mysql -h <host> -P <port> -u <user> -p <dbname> < seed_more.sql
   mysql -h <host> -P <port> -u <user> -p <dbname> < seed_more2.sql
   mysql -h <host> -P <port> -u <user> -p <dbname> < seed_bills.sql
   ```
3. Push this repo to GitHub.
4. On [render.com](https://render.com): **New → Blueprint**, select the repo
   (it reads `render.yaml`), or **New → Web Service** with:
   - Build: `pip install -r requirements.txt`
   - Start: `gunicorn app:app --bind 0.0.0.0:$PORT`
5. Add the `HMS_DB_*` environment variables from step 1 in the Render dashboard.
6. Deploy. Your site will be live at `https://<name>.onrender.com`.

## Project structure

```
app.py            # Flask entry point (app = create_app())
config.py         # env-driven settings
db.py             # MySQL connection pool + query/execute helpers
modules/          # patients, doctors, appointments, billing, analytics
templates/        # Jinja2 templates
static/           # css, js, images, generated charts + csv
sql/              # schema.sql + seed_*.sql (database setup)
scripts/          # push.sh (deploy helper)
cbse_project/     # CBSE Class 12 IP syllabus script (ip_project.py) + its outputs
Procfile          # gunicorn start command
render.yaml       # Render blueprint
requirements.txt  # Python dependencies
```
