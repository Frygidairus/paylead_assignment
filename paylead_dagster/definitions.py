import os

from dagster import asset, op, job, Definitions, resource
from dagster_docker import execute_docker_container
from sqlalchemy import create_engine
import pandas as pd


@resource(config_schema={"db_uri": str})
def db(init_context):
    """Lightweight SQLAlchemy engine resource (mock-friendly)."""
    uri = init_context.resource_config["db_uri"]
    return create_engine(uri)


@op
def run_normalize_container():
    """
    Lightweight op that launches the normalize-job container.
    Uses environment variables for quick local/mocked runs:
      - NORMALIZE_IMAGE (default: "normalize-job")
      - NORMALIZE_CHUNK_SIZE (default: "5000")
      - DATABASE_URI (optional)
    """
    image = os.environ.get("NORMALIZE_IMAGE", "normalize-job")
    chunk_size = os.environ.get("NORMALIZE_CHUNK_SIZE", "5000")
    database_uri = os.environ.get("DATABASE_URI")

    env_vars = {"DATABASE_URI": database_uri} if database_uri else None

    # keep streaming off for a light-weight mock; set stream_logs=True if you want logs
    result = execute_docker_container(
        image=image,
        command=[f"--chunk-size={chunk_size}"],
        env_vars=env_vars,
        stream_logs=False,
    )

    return result


@job
def normalize_job():
    run_normalize_container()


@asset(required_resource_keys={"db"})
def point_of_sales(context) -> pd.DataFrame:
    """
    Simple asset that loads the point_of_sales table as a pandas DataFrame.
    Intended as a mock / lightweight extractor for the project.
    Resource config example:
      resources:
        db:
          config:
            db_uri: "postgresql://user:pass@host.docker.internal:5432/paylead_db"
    """
    engine = context.resources.db
    df = pd.read_sql("SELECT * FROM point_of_sales", con=engine)
    context.log.info(f"Loaded {len(df)} rows from point_of_sales")
    return df


definitions = Definitions(
    assets=[point_of_sales],
    jobs=[normalize_job],
    resources={"db": db},
)