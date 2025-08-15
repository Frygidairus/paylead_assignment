# Software Data Engineer Take-Home Assignment - Paylead Knowledge Team

## Background

The Knowledge team at Paylead builds machine learning algorithms and features for transaction enrichment and user insights.

We deal with huge amounts of data to provide real-time merchant identification and categorization for banking transactions. Our work combines real-time NLP model inference, recommendation engines, and batch processing, making large-scale marketing targeting and better transaction understanding possible.

## Problem Statement

Build a data engineering system that handles Point of Sales with their address for transaction enrichment. Your solution should demonstrate proficiency in data modeling, API development, stream processing, and/or orchestration.

## Data

You'll work with the same datasets used by our Data Science team. You can download the data folder from our [GDrive](https://drive.google.com/file/d/1ee12NKfkaxZhGT8u16MMWyyZHyJOVS_p/view?usp=sharing)

1. **Official French business registry** – A sample from the complete database of registered French businesses.
2. **Partner store locations** – Scraped data from retail partners (like Carrefour stores).

### `etablissements.parquet` (French Business Registry)

- Parquet file with standardized French administrative data ~40M+ establishments

  | Field                    | Type   |
  | ------------------------ | ------ |
  | siret                    | String |
  | siren                    | String |
  | nic                      | String |
  | creation_date            | String |
  | is_active                | String |
  | naf_code                 | String |
  | establishment_name_0     | String |
  | establishment_name_1     | String |
  | establishment_name_2     | String |
  | establishment_name_3     | String |
  | street_number            | String |
  | repetition_index         | String |
  | street_type              | String |
  | street_name              | String |
  | zip_code                 | String |
  | city_name                | String |
  | latitude_coordinate      | String |
  | longitude_coordinate     | String |
  | is_head_quarter          | String |
  | employee_segment         | String |
  | current_state_start_date | String |
  | complement_address_1     | String |
  | complement_address_2     | String |

### `carrefour_hypermarche.csv` (Partner Store Data)

- CSV of all carrefour Point of Sales from Web scraping with varying data quality

  | Field         | Type   |
  | ------------- | ------ |
  | store_name    | String |
  | raw_address   | String |
  | street_number | String |
  | street        | String |
  | zip_code      | Int64  |
  | city          | String |

## Assignment

Build a simple application with a REST API and either a stream processor (like Kafka or RabbitMQ) or an orchestrator (like Dagster or Airflow). Store point of sales data in a SQL database. The API (using FastAPI or Flask) should support CRUD operations for point of sales

- Design a normalized SQL schema for French business point of sales.
  - The `point_of_sales` table should include at least two optional fields: `siret` and `store_name_normalized`.
- Implement REST API endpoints for managing point of sales and matches:
  - `GET /point_of_sales` – Search and filter point of sales
    - Optional - Filter and search by `siret` and `zip_code`.
  - `POST /point_of_sales` – Create a new point of sale
  - `GET /point_of_sales/{id}` – Get the associated point of sale
  - `PUT /point_of_sales/{id}` – Update a point of sale
  - `DELETE /point_of_sales/{id}` – Soft delete a point of sale
- Choose and implement one of the following:
  - Stream processor: After a `POST /point_of_sales` request, process and update point_of_sales data in real time. This should update the `store_name_normalized` field using the function provided below.
    OR
  - Orchestrator: Schedule and batch update recent entries in `point_of_sales` to update the `store_name_normalized` field using the function provided below.

```python
def normalize_store_name(store_name):
   import unicodedata
   normalized_store_name = store_name.lower().strip()
   normalized_store_name = unicodedata.normalize('NFKD', normalized_store_name).encode('ascii', 'ignore').decode('ascii')
   normalized_store_name = '-'.join(normalized_store_name.split())
   return normalized_store_name
```

## Deliverables

- Provide a Python package with the app and setup instructions. We should be able to launch it easily on a Mac or Linux
  - A section to setup the Database
  - A section to setup the API
  - A section to setup the Stream processor or Orchestrator
- A SQL `schema.sql` file with the current database schema
- A short technical writeup in markdown outlining your approach and choices

## Tips

- This test is all about helping you shine — no tricks, no gotchas, just a chance to show us what you’re great at. 
  Feel free to go beyond the brief and add any features or details you think will make your project stand out.

- Your work will be evaluated along the following dimensions:
  - Overall quality: Does it work? Is the code clear, maintainable, and easy to understand?
  - Technical decisions: The choices you made regarding the tools, data handling, and code structure.
  - Production readiness: While this won’t be deployed to production, we encourage you to treat it as if it could be.
    If you need to take shortcuts due to time constraints, feel free to explain what you would have done differently in a real-world scenario.
  - Don't underestimate the packaging of your project (how would you have packaged it in case of real-world situation)

