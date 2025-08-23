import logging
import os
import pandas as pd
from sqlalchemy import create_engine, text
import unicodedata


logging.basicConfig(
    level=logging.INFO,  # Show INFO and above
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)

logger = logging.getLogger(__name__)
# Connection string
DATABASE_URL = os.getenv("DATABASE_URI", "postgresql://admin:adminpass@localhost:5432/paylead_db")
engine = create_engine(DATABASE_URL)


# Function to normalize store names
def normalize_store_name(store_name):
   
   normalized_store_name = store_name.lower().strip()
   normalized_store_name = unicodedata.normalize('NFKD', normalized_store_name).encode('ascii', 'ignore').decode('ascii')
   normalized_store_name = '-'.join(normalized_store_name.split())
   return normalized_store_name

# Update existing records in bulk
def normalize_new_stores(chunk_size=50000):
    logger.info("Normalization process started...")
    with engine.begin() as conn:
        # Load all rows needing normalization into a DataFrame
        chunks = pd.read_sql(
            text("SELECT id, store_name FROM point_of_sales WHERE store_name_normalized IS NULL"),
            conn, chunksize=chunk_size
        )

        total_updated = 0
        for i, chunk in enumerate(chunks, start=1):
            logger.info(f"Processing chunk {i}, {len(chunk)} rows")

            # Normalize store_name for this chunk
            chunk["store_name_normalized"] = chunk["store_name"].apply(normalize_store_name)

            # Prepare dicts for batch update
            updates = chunk[["id", "store_name_normalized"]].to_dict(orient="records")

            conn.execute(
                text("UPDATE point_of_sales SET store_name_normalized = :store_name_normalized WHERE id = :id"),
                updates
            )

            total_updated += len(updates)
            logger.info(f"Updated {total_updated} rows total")

        logger.info(f"Total updated: {total_updated}")

if __name__ == "__main__":
    normalize_new_stores()