import os
import pandas as pd
from pyarrow import parquet as pq
from sqlalchemy import create_engine, text
import logging

logging.basicConfig(
    level=logging.INFO,  # Show INFO and above
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)

logger = logging.getLogger(__name__)
# Connection string
DATABASE_URL = os.getenv("DATABASE_URI", "postgresql://admin:adminpass@localhost:5432/paylead_db")
engine = create_engine(DATABASE_URL)

CARREFOUR_CSV = "data/carrefour_hypermarche.csv"
ETABLISSEMENTS_PARQUET = "data/etablissements.parquet"

def load_carrefour():

    logger.info("Loading Carrefour CSV...")
    df = pd.read_csv(CARREFOUR_CSV)

    # Normalize column names
    df = df.rename(columns={
        "store_name": "store_name",
        "street_number": "street_number",
        "street": "street",
        "zip_code": "zip_code",
        "city": "city"
    })

    # Keep only the columns relevant for our schema
    df = df[["store_name", "street_number", "street", "zip_code", "city"]]

    # Insert into DB
    df.to_sql("point_of_sales", engine, if_exists="append", index=False)
    logger.info(f"Inserted {len(df)} rows from Carrefour CSV")


def load_etablissements(batch_size=5000, limit=5000000):

    inserted = 0

    logger.info("Loading Etablissements Parquet...")
    for batch in pq.ParquetFile(ETABLISSEMENTS_PARQUET).iter_batches(batch_size=batch_size):
        df = batch.to_pandas()
        # Keep only necessary columns
        df = df[[
            "siret",
            "establishment_name_0",
            "establishment_name_1",
            "establishment_name_2",
            "establishment_name_3",
            "street_number",
            "street_name",
            "zip_code",
            "city_name",
            "latitude_coordinate",
            "longitude_coordinate"
        ]]

        name_cols = [
            "establishment_name_0",
            "establishment_name_1",
            "establishment_name_2",
            "establishment_name_3"
            ]

        # For each name rows, pick the first non-empty value
        df["store_name"] = df[name_cols].apply(
            lambda row: next((x for x in row if pd.notna(x) and x != ""), ""), axis=1)
        
        # Keep only rows where a store_name exists
        df = df[df["store_name"] != ""]

        # Drop original name columns
        df = df.drop(columns=name_cols)

        df = df.rename(columns={
            "siret": "siret",
            "street_number": "street_number",
            "street_name": "street",
            "zip_code": "zip_code",
            "city_name": "city",
            "latitude_coordinate": "latitude",
            "longitude_coordinate": "longitude",
        })
        # Convert latitude and longitude to numeric, coercing errors to NaN
        df["latitude"] = pd.to_numeric(df["latitude"], errors="coerce")
        df["longitude"] = pd.to_numeric(df["longitude"], errors="coerce")

        # Insert into DB
        df.to_sql("point_of_sales", engine, if_exists="append", index=False)

        inserted += len(df)

        logger.info(f"Inserted {len(df)} rows from Etablissements Parquet")
        
        if inserted >= limit:
            logger.info(f"Reached limit of {limit} rows, stopping further inserts.")
            break

    logger.info("Finished loading Etablissements Parquet: {inserted} rows inserted")

def populate():
    #load_carrefour()
    load_etablissements()


if __name__ == "__main__":
    populate()