# Engineering Decisions

I record the main technical decisions so the repository explains both the implementation and the reasoning behind it.

## ADR-001 — Medallion architecture

**Status:** Accepted

I use Bronze, Silver and Gold to separate source preservation, data standardization and analytical serving.

## ADR-002 — Delta tables for curated layers

**Status:** Accepted

I use Delta tables for Silver and will use them for Gold so curated datasets can support reliable schema handling, transactional writes and future MERGE/upsert patterns.

## ADR-003 — Raw API payloads in Lakehouse Files

**Status:** Accepted

I store REST payloads under Lakehouse `Files/bronze` instead of converting them immediately into curated tables. This preserves the original source response before transformation logic is applied.

Current objects:

```text
Files/bronze/opendata/district_data/district_data.json
Files/bronze/citybikes/bicing/bicing_snapshot.json
```

## ADR-004 — Fabric Data Factory for ingestion orchestration

**Status:** Accepted

I use Fabric pipelines and Copy activities for source ingestion so extraction can be parameterized, scheduled, monitored and chained with notebook activities.

## ADR-005 — CKAN API as the first stable ingestion source

**Status:** Accepted for the first milestone

I tested Bicing's public GBFS API first, but the upstream API returned a temporary HTTP 503 block when called through Fabric. I switched the first operational ingestion to Barcelona Open Data's CKAN API so the Bronze architecture could be validated independently of that upstream limitation.

## ADR-006 — Preserve source codes as strings in Silver

**Status:** Accepted

Fields such as district, neighborhood, census section and nationality codes may contain numeric-looking values, but semantically they are identifiers. I keep them as strings in Silver to preserve their meaning and avoid accidental arithmetic.

## ADR-007 — Name the first curated table by its actual grain

**Status:** Accepted

I use `silver_district_context` instead of `silver_districts` because the source contains multiple observations per district across census sections, neighborhoods and nationality categories.

## ADR-008 — Use CityBikes as the operational Bicing REST source

**Status:** Accepted

I use the CityBikes network endpoint for the current Bicing ingestion because it exposes station-level availability through a stable REST response that Fabric can ingest directly.

The endpoint provides the nested `network.stations` array required for station-level mobility analysis.

## ADR-009 — Separate initial snapshot ingestion from historical snapshot design

**Status:** Accepted

I currently persist the first Bicing payload as `bicing_snapshot.json` to validate ingestion independently from incremental design.

I will add timestamped or partitioned snapshot persistence before implementing historical station analysis. This keeps the initial milestone simple without presenting a single overwritten file as a completed historical ingestion strategy.
