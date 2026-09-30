# Engineering Decisions

I record the main technical decisions here so the repository explains not only what I built, but why I built it this way.

## ADR-001 — Medallion architecture

**Status:** Accepted

I chose Bronze, Silver and Gold to separate source preservation, data standardization and analytical serving.

## ADR-002 — Delta tables for curated layers

**Status:** Accepted

I use Delta tables for Silver and will use them for Gold so curated datasets can support reliable schema handling, transactional writes and future MERGE/upsert patterns.

## ADR-003 — Raw API payloads in Lakehouse Files

**Status:** Accepted

I store REST payloads under Lakehouse `Files/bronze` rather than immediately converting them into tables. This preserves the original source response before business transformations are applied.

Current object:

```text
Files/bronze/opendata/district_data/district_data.json
```

## ADR-004 — Fabric Data Factory for ingestion orchestration

**Status:** Accepted

I use a Fabric pipeline and Copy activity for source ingestion so extraction can later be parameterized, scheduled, monitored and chained with notebook activities.

## ADR-005 — CKAN API as the first stable ingestion source

**Status:** Accepted for the first milestone

I tested Bicing's public GBFS API first, but the upstream API returned a temporary HTTP 503 block when called through Fabric. I switched the first operational ingestion to Barcelona Open Data's CKAN API so the Bronze architecture could be validated independently of that upstream limitation.

This decision does not remove Bicing from the target architecture; it only decouples the first pipeline milestone from temporary upstream behavior.

## ADR-006 — Preserve source codes as strings in Silver

**Status:** Accepted

Fields such as district, neighborhood, census section and nationality codes may contain numeric-looking values, but semantically they are identifiers. I therefore keep them as strings in Silver to avoid accidental arithmetic and to preserve identifier semantics.

## ADR-007 — Name the first curated table by its actual grain

**Status:** Accepted

I use `silver_district_context` instead of `silver_districts` because the source contains multiple observations per district across census sections, neighborhoods and nationality categories. The table name should describe the data accurately rather than imply one row per district.
