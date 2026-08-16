# PostgreSQL Vector Similarity Search

## Description

This project implements a text similarity search system using PostgreSQL with the pgvector extension. Text records describing property listings (apartments, studios, villas, duplexes with attributes like city, bedrooms, bathrooms, and size) are embedded into 384-dimensional vectors using a local sentence-transformers model, then stored in a Postgres table with a `vector` column. A new query text is embedded the same way and compared against the stored vectors using distance search to retrieve the most similar listings.

## Requirements

- Python 3.14
- PostgreSQL 18
- pgvector extension (v0.8.6, built from source on Windows)
- psycopg2-binary
- pgvector (Python package)
- langchain-huggingface
- sentence-transformers
- numpy

Install all requirements with:

```
pip install psycopg2-binary pgvector langchain-huggingface sentence-transformers numpy
```

## Topics Learned

- Building and installing the pgvector Postgres extension from source on Windows (MSVC toolchain, `nmake`, `PGROOT`, Windows SDK dependency)
- Designing a Postgres schema with a native `vector(N)` column type, and matching column dimension to the embedding model's output size
- Generating sentence embeddings locally with a HuggingFace sentence-transformers model (`all-MiniLM-L6-v2`), avoiding external embedding API dependencies
- Batch embedding with `embed_documents()` vs single-query embedding with `embed_query()`, and why they're not interchangeable
- Registering the `pgvector` psycopg2 adapter (`register_vector`) to correctly serialize Python/numpy arrays into Postgres `vector` values
- Writing nearest-neighbor similarity queries using pgvector's distance operators (`<->` for L2, `<=>` for cosine)
- Parameterized query execution with psycopg2, including correct tuple-wrapping of query parameters

## Challenges
- **Vector shape mismatches**: Inserts initially failed with `expected ndim to be 1` and `can't adapt type 'numpy.ndarray'` errors, caused by embedding a single string through `embed_documents()` inside a loop (producing nested/incorrectly-shaped arrays) instead of batching the whole list in one call, combined with a missing `register_vector()` call on the psycopg2 connection.
- **Database/table mismatches**: Several early runs failed because the Python script's connection string pointed at a different database name than the one the table was actually created in via pgAdmin — resolved by explicitly confirming the active database with `current_database()`.
- **API key/provider confusion**: Initial attempts to use a hosted embedding API (NVIDIA NIM) failed repeatedly due to key/endpoint mismatches (wrong key type, missing `base_url` override). Switched to local sentence-transformers embeddings to remove the external API dependency entirely — no cost, no rate limits, no auth issues.

## How to Run

1. Clone or download this repository.
2. Install PostgreSQL 18 and build/install the pgvector extension for your platform.
3. Install the required Python libraries (see Requirements above).
4. Create the database and enable the extension:

```sql
CREATE DATABASE ragdb;
CREATE EXTENSION IF NOT EXISTS vector;
```

5. Create the `items` table:

```sql
CREATE TABLE IF NOT EXISTS items (
    id SERIAL PRIMARY KEY,
    content VARCHAR(255) NOT NULL,
    embedding vector(384)
);
```

6. Run the script:

```
python main.py
```