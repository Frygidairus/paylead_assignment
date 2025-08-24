# paylead_assignment

Small Flask API and ETL job suite to ingest, normalize and store point-of-sale data.

## Overview
- Flask app exposing a minimal CRUD API for point-of-sale records.
- Jobs to populate and normalize the database from source files (CSV / Parquet).
- Postgres as the primary datastore.
- Designed to run in Docker. Jobs can be scheduled via host scheduler or run as ephemeral containers.

## Repository layout
- app/ — Flask application
  - app.py — application factory / startup
  - config.py — configuration
  - models.py — SQLAlchemy models
  - routes/ — api blueprints (health, pos)
- jobs/ — ETL scripts (populate_db.py, normalize_db.py)
- data/ — input files (etablissements.parquet, carrefour_hypermarche.csv to be manually added)
- dockerfile — web app image
- docker-compose.yml — services manifest
- requirements.txt — Python dependencies

## Quickstart — Local (VS Code / terminal)
1. Create and activate virtualenv:
   ```
   python -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```
2. Ensure data files exist in `data/` (or set env vars to point them).
3. Start Postgres (compose or external) and run the app:
   ```
   export DATABASE_URI="postgresql://admin:adminpass@localhost:5432/paylead_db"
   python app/app.py
   ```
4. Run jobs manually:
   ```
   python jobs/populate_db.py
   python jobs/normalize_db.py
   ```

## Docker
- Start DB and app:
  ```
  docker-compose up -d 
  ```
