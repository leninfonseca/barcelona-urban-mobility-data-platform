# Engineering Decisions

I record the main technical decisions here so the repository explains not only what I built, but why I built it this way.

## ADR-001 — Medallion architecture

**Status:** Accepted

I chose Bronze, Silver and Gold to separate source preservation, data standardization and analytical serving.

## ADR-002 — Delta tables for curated layers

**Status:** Accepted

I will use Delta tables for Silver and Gold so curated datasets can support reliable schema handling, transactional writes and future MERGE/upsert patterns.

## ADR-003 — Raw API payloads in Lakehouse Files

**Status:** Accepted

I store the first REST payload under Lakehouse `Files/bronze` rather than immediately converting it into a table. This preserves the original source response before business transformations are applied.

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

This decision does not remove Bicing from the target architecture; it only decouples the first pipeline milestone from the temporary API behavior.
