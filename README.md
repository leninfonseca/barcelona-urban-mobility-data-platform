# Barcelona Urban Mobility Data Platform

End-to-end Data Engineering project built with Microsoft Fabric to ingest, transform, model and serve Barcelona urban mobility data.

## Project goals

This project is designed to practice production-oriented Data Engineering concepts using Microsoft Fabric:

- Data ingestion and orchestration with Fabric Data Factory pipelines
- Lakehouse architecture with OneLake and Delta tables
- Medallion architecture: Bronze, Silver and Gold
- Data transformation with PySpark notebooks
- Analytical modeling and querying with SQL
- Incremental data loads and data quality controls
- Documentation of architecture and engineering decisions

## Architecture

```text
Barcelona Open Data / APIs / CSV / JSON
                 |
                 v
        Fabric Data Pipeline
                 |
                 v
              Bronze
                 |
          PySpark Notebooks
                 |
                 v
              Silver
                 |
        PySpark + SQL
                 |
                 v
               Gold
                 |
                 v
      SQL Analytics Endpoint
```

## Repository structure

- `architecture/` — architecture diagrams and design documentation
- `notebooks/` — Fabric/PySpark notebooks
- `sql/` — SQL modeling and analytical queries
- `pipelines/` — pipeline documentation and configuration notes
- `docs/` — data model, data quality and engineering decisions
- `tests/` — validation and data-quality tests

## Status

🚧 In development.

The project will be built incrementally while learning Microsoft Fabric and preparing for real-world Azure/Fabric Data Engineering work.
