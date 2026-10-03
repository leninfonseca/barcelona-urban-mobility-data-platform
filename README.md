# Barcelona Urban Mobility Data Platform

I am building an end-to-end Data Engineering platform in Microsoft Fabric around Barcelona public data.

## Current state

Two REST ingestion paths are operational and both reach Silver.

### Contextual district data
- Pipeline: `pl_ingest_mobility_bronze`
- Bronze: `Files/bronze/opendata/district_data/district_data.json`
- Notebook: `nb_bronze_to_silver_districts`
- Silver: `silver_district_context`

### Bicing mobility data
- Source: CityBikes Bicing REST API
- Pipeline: `pl_ingest_bicing_bronze`
- Bronze history: timestamped JSON snapshots partitioned by year/month/day
- Notebook: `nb_bicing_snapshot_history`
- Historical Silver: `silver_bicing_station_history`
- Incremental strategy: watermark + Delta MERGE
- Orchestration: Copy activity → Notebook activity

## Bicing historical flow

```text
CityBikes API
→ timestamped Bronze snapshot
→ watermark detection
→ read only new snapshots
→ PySpark transformation
→ data quality checks
→ Delta MERGE
→ silver_bicing_station_history
```

Historical grain: `station_id + snapshot_ingested_at`.

The notebook supports bootstrap and incremental execution, exits successfully when there is no new data, and reprocessing the same batch does not create duplicates.

## Data quality

Critical rules stop processing. Non-critical source inconsistencies are preserved through warnings and `bike_breakdown_valid`.

See [Data Quality](docs/data-quality.md) and [Troubleshooting](docs/troubleshooting.md).

## Evidence

Historical/incremental screenshots:
- `13-bicing-bronze-history.png`
- `14-bicing-incremental-merge.png`
- `15-bicing-end-to-end-pipeline.png`

## Status

**Bronze and Silver are operational, including historical incremental Bicing processing and end-to-end orchestration.**

Next milestone: Gold modeling, SQL analytics and analytical serving.
