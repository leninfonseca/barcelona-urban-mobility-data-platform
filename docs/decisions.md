# Engineering Decisions

## ADR-001 — Medallion architecture
**Status:** Accepted

Bronze preserves source data, Silver standardizes and validates it, and Gold serves analytics.

## ADR-002 — Delta for curated layers
**Status:** Accepted

Delta supports transactional writes and MERGE-based incremental processing.

## ADR-003 — Immutable timestamped Bicing snapshots
**Status:** Accepted

Each ingestion creates a new JSON under year/month/day partitions instead of overwriting one file.

## ADR-004 — Historical grain uses ingestion snapshot time
**Status:** Accepted

`source_timestamp` belongs to the upstream source and can remain unchanged across two captures.

Historical key:

```text
station_id + snapshot_ingested_at
```

## ADR-005 — Watermark-based incremental processing
**Status:** Accepted

`MAX(snapshot_ingested_at)` identifies the latest processed snapshot. Only newer Bronze files are read.

## ADR-006 — Idempotent Delta MERGE
**Status:** Accepted

Matched historical observations are left unchanged; only unmatched observations are inserted.

## ADR-007 — No-new-data is successful
**Status:** Accepted

If no Bronze file is newer than the watermark, the notebook exits successfully.

## ADR-008 — Copy before Notebook
**Status:** Accepted

The Bicing historical notebook activity runs only after the Bronze Copy activity succeeds.

## ADR-009 — Critical vs warning quality rules
**Status:** Accepted

Critical schema/value failures stop processing. Bike-breakdown inconsistencies are preserved as warnings and flags.

## ADR-010 — Gold uses a star schema
**Status:** Accepted

The Bicing analytical model separates measurable historical observations from descriptive dimensions.

`gold_fact_bicing_availability` is the central fact table, linked to station, date and time dimensions.

## ADR-011 — Deterministic station surrogate key
**Status:** Accepted

Gold uses:

```text
xxhash64(station_id)
```

to generate `station_key`.

The source `station_id` is retained as the natural/business identifier, while `station_key` belongs to the analytical model.

## ADR-012 — Latest-known station dimension
**Status:** Accepted

`gold_dim_station` keeps one row per station using the latest `snapshot_ingested_at` available in Silver.

The current project does not implement SCD Type 2 for station attributes.

## ADR-013 — Full Gold rebuild from Silver
**Status:** Accepted

Silver remains incrementally maintained and is the historical source of truth.

Gold is rebuilt with Delta overwrite from the complete validated Silver history.

For the current data volume this is simpler and safer than maintaining a second incremental state layer.

## ADR-014 — Do not force district enrichment
**Status:** Accepted

The contextual district dataset and Bicing history currently have no reliable direct key.

The project does not join station names to neighborhood or district names heuristically.

A future implementation may add geographic polygons and perform a real spatial mapping from Bicing coordinates to districts/neighborhoods.

## ADR-015 — Use the SQL Analytics Endpoint as the analytical serving surface
**Status:** Accepted

The Gold Delta tables are consumed directly through the Fabric SQL Analytics Endpoint.

This avoids creating a duplicate analytical database solely for SQL access and keeps the SQL layer aligned with the same Gold tables produced by Spark.

## ADR-016 — Keep the physical Gold model dimensional and expose a denormalized BI query
**Status:** Accepted

The underlying Gold layer remains a star schema.

For downstream BI, `06_powerbi_serving_query.sql` joins the fact with station, date and time dimensions and exposes a convenient denormalized result.

This keeps dimensional modeling concerns separate from consumer convenience.

## ADR-017 — Availability status is a serving-layer classification
**Status:** Accepted

The SQL serving query classifies each observation with ordered `CASE` logic:

```text
Offline
No capacity
Low bikes
Low docks
Balanced
```

The 20% low-availability thresholds are analytical rules for the current dashboard layer, not corrections to the source data and not Silver quality rules.
