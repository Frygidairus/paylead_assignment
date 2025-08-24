# app — Flask application

Small Flask API serving point-of-sale data and DB models used by the project jobs.

## Purpose
Provide an HTTP API to create/list/read/update/delete point-of-sale records and a simple health check.

## Files
- app.py — application factory and startup; registers blueprints and runs db.create_all()
- config.py — configuration (reads DATABASE_URI)
- models.py — SQLAlchemy models (PointOfSale)
- routes/
  - health.py — GET /health
  - pos.py — CRUD endpoints for /point_of_sales

## Environment
- DATABASE_URI — SQLAlchemy connection string
  - Default: postgresql://admin:adminpass@localhost:5432/paylead_db

## Quick start (dev)
1. Create venv and install deps:
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```
2. Ensure DATABASE_URI points to a running Postgres instance (or use the compose postgres).
3. Run the app:
   ```bash
   # option A — run directly (used in repo)
   python app/app.py

   # option B — via flask CLI
   export FLASK_APP=app:create_app
   flask run --host=0.0.0.0 --port=5000
   ```

## Endpoints (examples)
- Health
  - GET /health
  - Response: 200 { "status": "ok" }

- Point of sales
  - POST /point_of_sales
    - JSON body example:
      ```json
      {
        "store_name": "Carrefour Test",
        "siret": "12345678901234",
        "street_number": "10",
        "street": "Rue Exemple",
        "zip_code": "75001",
        "city": "Paris",
        "latitude": "48.8566",
        "longitude": "2.3522"
      }
      ```
  - GET /point_of_sales — list (supports pagination/filters if implemented)
  - GET /point_of_sales/<id> — retrieve
  - PUT /point_of_sales/<id> — update JSON body same as POST
  - DELETE /point_of_sales/<id> — soft delete (is_deleted True)

cURL example — create:
```bash
curl -X POST http://localhost:5000/point_of_sales \
  -H "Content-Type: application/json" \
  -d '{"store_name":"Carrefour Test","zip_code":"75001","city":"Paris"}'
```

## Database
- Models live in models.py; create_all() is run on app startup (see app.create_app).
- For migrations you can add Alembic later; currently schema changes are applied via create_all().

## Notes & recommendations
- Ensure SQLALCHEMY_DATABASE_URI is set in your environment when running in production or CI.
- Add input validation and error handling in routes/pos.py (currently scaffolded).
- Add unit tests for routes and models under a tests/ directory.
- When running in Docker, the dockerfile sets FLASK_APP to `app:create_app` — keep