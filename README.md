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
  - config.py — configuration (see for default DATABASE_URI and other env vars)
  - models.py — SQLAlchemy models
  - routes/ — api blueprints (health, pos)
- jobs/ — ETL scripts
  - populate_db.py — initial population job
  - normalize_job/ — normalization job (includes job/main.py which can be run locally)
- data/ — input files (etablissements.parquet, carrefour_hypermarche.csv to be manually added)
- app/Dockerfile — web app image (note: not a top-level Dockerfile)
- docker-compose.yml — services manifest
- requirements.txt — Python dependencies

## Quickstart — Local (VS Code / terminal)
1. Create and activate virtualenv:
   ```
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```
2. Ensure data files exist in `data/` (or set env vars to point them).
3. Start Postgres DB and app:
  ```
  docker-compose up -d 
  ```
3. Run populate job manually (may take several minutes):
   ```
   python jobs/populate_db.py
  
   ```
4. Create a few random point of sale (using the Postman collection?)
5. Run this script to build the Docker image to normalize the new names:
``` bash
docker build -t normalize-job -f jobs/normalize_job/build/Dockerfile jobs/normalize_job
```
6. Run the image created:
``` bash
docker run -it normalize-job
```

## NB
- the endpoint 127.0.0.1:5001/health will return 'ok' if the API is up and running.
- the API can be run manually using:
```
python app/app.py
```
- it is possible to query the db inside its container using the command:
``` bash
docker exec -it paylead_postgres psql -U admin -d paylead_db
```
## WARNINGS
- depending on your Docker setup, a very large query may crash the API (exited with code 137), indicating Docker did not have enough RAM to process the query 