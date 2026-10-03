# Engineering Decisions

## ADR-001 — Medallion architecture
**Status:** Accepted

Bronze preserves source data, Silver standardizes it, and Gold serves analytics.

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

## ADR-008 — Copy before Notebook
**Status:** Accepted

The Bicing notebook activity runs only after the Bronze Copy activity succeeds.

## ADR-009 — Critical vs warning quality rules
**Status:** Accepted

Critical schema/value failures stop processing. Bike-breakdown inconsistencies are preserved as warnings and flags.
