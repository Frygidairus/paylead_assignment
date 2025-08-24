# Normalize Job (jobs/normalize_job)

Small batch job to compute and persist normalized store names for entries in the `point_of_sales` table.

Overview
- Reads rows where `store_name_normalized` is NULL, normalizes `store_name`, and updates the DB in chunks.
- Primary logic: [`normalize_db.normalize_new_stores`](jobs/normalize_job/job/normalize_db.py).
- Normalization function: [`normalize_db.normalize_store_name`](jobs/normalize_job/job/normalize_db.py).

# How to test?
## Create the Docker image
Run this script to build the Docker image:
``` bash
docker build -t normalize-job -f jobs/normalize_job/build/Dockerfile jobs/normalize_job
```

## Run the image 
Run the image created (and outputs verbose thanks to the -it flag):
``` bash
docker run -it normalize-job
```

## Possible improvements
- Add dynamic paths and especially dynamic DATABASE_URI so it can be run locally using:
```bash
python jobs/normalize_job/job/main.py 
```