### The DataBase
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

