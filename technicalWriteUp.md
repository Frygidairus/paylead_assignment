# The DataBase
## PostgreSQL
The decision to use PostgreSQL as database has been motivated by two main factors:
- It is an open source and widely used database
- It is already part of the Paylead's stack

Rather easy to implement using a Docker container, PostgreSQL seems to be a great choice for this exercise.

## The schema 
The goal is to create a normalized SQL database.
  
| Column                  | Type                        | Description / Notes                            |
| ----------------------- | --------------------------- | ---------------------------------------------- |
| id                      | SERIAL                      | Primary key                                    |
| siret                   | VARCHAR(14)                 | SIRET number (optional)                        |
| store\_name             | TEXT                        | Store name (required)                          |
| store\_name\_normalized | TEXT                        | Normalized store name (optional)               |
| street\_number          | VARCHAR(10)                 | Street number                                  |
| street                  | TEXT                        | Street name                                    |
| zip\_code               | VARCHAR(6)                  | Zip code (max 6 chars for French postal codes) |
| city                    | TEXT                        | City name                                      |
| latitude                | DOUBLE PRECISION            | Geographic latitude                            |
| longitude               | DOUBLE PRECISION            | Geographic longitude                           |
| is\_deleted             | BOOLEAN                     | Soft delete flag, default FALSE                |
| created\_at             | TIMESTAMP WITHOUT TIME ZONE | Creation timestamp, default NOW()              |
| updated\_at             | TIMESTAMP WITHOUT TIME ZONE | Last update timestamp, default NOW()           |

This database should store and provide enough info to identify the different points of sale and manage them.

It is a Third Normal Form table. 

In order to speed up the search and filtering processes, two indices are used:
- an index on the SIRET number 
- an index on the zip code

## The initial insertion

Inserting data into the database when initiating the project is done thanks to the _populate\_db.py_ script.

- data from the .csv is inserted directly as it is light weight
- data from the .parquet is broken down in batches (5,000 rows each by default) as the file is several millions rows

More than 33M rows where _establishment\_name\_0_ is empty. Tried to fallback on the other establishment names, still 30M empty.
Some rows contain "[ND]" as _store\_name_. This seems to be a placeholder for unknown names, hence these rows are excluded.

In order to speed up the process of initial insertion, and for demonstration purposes, a 5 million rows limit is set as default. 

# The API
## Flask
Flask is a simple and easy to use web framework for Python. Once more, as it already part of Paylead's stack, it seemed to be a great choice to develop the API.
## Endpoints
The whole API code is located in the _app_ folder. SQLAlchemy is used to create a connection with the database.
The routes are in the folder _routes_ where, in addition to the 5 mandatory endpoints, a health endpoint allow to check if the API is up and running, returning a simple 'ok' when it is.
## Containerization
The API is containerized and is run when the postgres container is up. A retry loop regarding the connection to the db is in place as the API container may sometimes be faster than the DB container at launch. This could also be handled using a health_check on the postgres container as a condition in the _docker-compose.yml_ for the API container.

# Orchestration
## jobs
The _jobs_ folder contains the jobs to be orchestrated. Here, only one job exists: _normalize\_db_. It has its own folder, is containerized, basically stands alone. There are several advantages to this, such as easier dependency management (avoiding a larger requirements, favorising requirements for each job), easier testing and CI/CD integration.

## Dagster
It can be noticed that no Dagster (or Airflow) instance is in the project. This has been done in order to keep it lighter weight. As the jobs are containerized, they are easily executed and orchestrated using [dagster-docker](https://docs.dagster.io/api/libraries/dagster-docker). 

## Assets
The choice of not adding a Dagster instance was also motivated by the fact that, at the moment, the project only contains a single asset: the point_of_sales table. 
The transformation (adding normalized names) is a simple UPDATE of the table.