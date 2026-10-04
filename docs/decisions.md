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

Historical key: `station_id + snapshot_ingested_at`.

## ADR-005 — Watermark-based incremental processing
**Status:** Accepted

`MAX(snapshot_ingested_at)` identifies the latest processed snapshot. Only newer Bronze files are read.

## ADR-006 — Idempotent Delta MERGE
**Status:** Accepted

Matched historical observations are left unchanged; only unmatched observations are inserted.

## ADR-007 — No-new-data is successful
**Status:** Accepted

If no Bronze file is newer than the watermark, the notebook exits successfully.

## ADR-008 — Copy before Silver notebook
**Status:** Accepted

Historical Silver processing runs only after Bronze Copy succeeds.

## ADR-009 — Critical vs warning quality rules
**Status:** Accepted

Critical schema/value failures stop processing. Bike-breakdown inconsistencies are preserved as warnings and flags.

## ADR-010 — Gold uses a star schema
**Status:** Accepted

The analytical model separates measurable historical observations from descriptive station/date/time dimensions.

## ADR-011 — Deterministic station surrogate key
**Status:** Accepted

Gold uses `xxhash64(station_id)` for `station_key` while retaining the source `station_id` as the natural key.

## ADR-012 — Latest-known station dimension
**Status:** Accepted

`gold_dim_station` keeps one row per station using the latest available Silver observation.

The current project does not implement SCD Type 2 for station attributes.

## ADR-013 — Full Gold rebuild from Silver
**Status:** Accepted

Silver remains incrementally maintained and is the historical source of truth.

For the current data volume, rebuilding Gold with Delta overwrite is simpler and safer than maintaining a second incremental state layer.

## ADR-014 — Do not force district enrichment
**Status:** Accepted

The contextual district dataset and Bicing history currently have no reliable direct key.

The project does not join station names to geographic areas heuristically.

## ADR-015 — SQL Analytics Endpoint as SQL serving surface
**Status:** Accepted

The Gold Delta tables are consumed directly through Fabric's SQL Analytics Endpoint instead of copying them into a separate analytical database.

## ADR-016 — Keep Gold dimensional and expose a denormalized SQL serving query
**Status:** Accepted

The physical Gold layer remains a star schema.

`06_powerbi_serving_query.sql` provides a consumer-friendly flattened projection without replacing the dimensional model.

## ADR-017 — Availability status is a serving-layer classification
**Status:** Accepted

The SQL serving query derives `Offline`, `No capacity`, `Low bikes`, `Low docks` and `Balanced` using ordered `CASE` logic.

The 20% thresholds are analytical rules, not Silver quality corrections.

## ADR-018 — Power BI consumes the Gold star schema directly
**Status:** Accepted

The primary Power BI semantic model uses `gold_dim_station`, `gold_dim_date`, `gold_dim_time` and `gold_fact_bicing_availability` directly.

The SQL flattened query remains a valid serving artifact but is not used to replace the dimensional model inside Power BI.

## ADR-019 — Single-direction 1:* semantic-model relationships
**Status:** Accepted

Each dimension key is unique and filters the fact through a one-to-many relationship.

Cross-filter direction remains single from dimension to fact to keep filter propagation predictable.

## ADR-020 — Weighted DAX availability measures
**Status:** Accepted

Network-level availability is calculated with ratios of sums:

```text
SUM(free_bikes) / SUM(station_capacity)
SUM(empty_slots) / SUM(station_capacity)
SUM(ebikes) / SUM(free_bikes)
```

This weights stations by the relevant base quantity instead of taking a simple average of row-level percentages.

## ADR-021 — Gold runs only after Silver succeeds
**Status:** Accepted

The final Fabric orchestration chains Bronze Copy → historical Silver processing → Gold analytical build with success dependencies.

This prevents Gold from rebuilding on top of a failed or incomplete Silver run.

## ADR-022 — Keep permanent visual evidence independent of Fabric availability
**Status:** Accepted

The repository includes a GIF and screenshots of the final Power BI report.

The downloaded PBIX is retained as the original live-connected report artifact, but the visual evidence does not depend on the Fabric workspace remaining available.
