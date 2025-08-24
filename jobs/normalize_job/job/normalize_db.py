import pandas as pd
from sqlalchemy import text
import unicodedata

from utils.db_handler import get_engine
from utils.logging_handler import get_logger


logger = get_logger()

engine = get_engine()


# Function to normalize store names
def normalize_store_name(store_name):
    if store_name is None:
        return None
    
    normalized_store_name = store_name.lower().strip()
    normalized_store_name = unicodedata.normalize('NFKD', normalized_store_name).encode('ascii', 'ignore').decode('ascii')
    normalized_store_name = '-'.join(normalized_store_name.split())
    return normalized_store_name


# Update existing records in bulk
def normalize_new_stores(chunk_size=5000):
    logger.info("Normalization process started...")
    
    # First, get the data outside of the transaction
    try:
        # Get all IDs that need normalization
        with engine.connect() as conn:
            count_result = conn.execute(
                text("SELECT COUNT(*) FROM point_of_sales WHERE store_name_normalized IS NULL")
            )
            total_count = count_result.scalar()
            logger.info(f"Found {total_count} rows to normalize")
            
            if total_count == 0:
                logger.info("No rows need normalization")
                return

        # Process in chunks
        total_updated = 0
        offset = 0
        
        while offset < total_count:
            logger.info(f"Processing chunk starting at offset {offset}")
            
            # Read chunk of data
            with engine.connect() as conn:
                chunk_df = pd.read_sql(
                    text("""
                        SELECT id, store_name 
                        FROM point_of_sales 
                        WHERE store_name_normalized IS NULL 
                        ORDER BY id 
                        LIMIT :limit OFFSET :offset
                    """),
                    conn,
                    params={"limit": chunk_size, "offset": offset}
                )
            
            if chunk_df.empty:
                logger.info("No more data to process")
                break
                
            logger.info(f"Loaded {len(chunk_df)} rows for processing")
            
            # Normalize store_name for this chunk
            chunk_df["store_name_normalized"] = chunk_df["store_name"].apply(normalize_store_name)
            
            # Update the database
            with engine.begin() as conn:
                updates = chunk_df[["id", "store_name_normalized"]].to_dict(orient="records")
                
                if updates:
                    conn.execute(
                        text("UPDATE point_of_sales SET store_name_normalized = :store_name_normalized WHERE id = :id"),
                        updates
                    )
                    
                    total_updated += len(updates)
                    logger.info(f"Updated {len(updates)} rows. Total updated: {total_updated}")
            
            offset += chunk_size
            
            # Safety check to avoid infinite loop
            if len(chunk_df) < chunk_size:
                break

        logger.info(f"Normalization process completed. Total updated: {total_updated}")
        
    except Exception as e:
        logger.error(f"Error during normalization: {e}")
        raise