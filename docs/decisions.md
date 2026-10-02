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

I store REST payloads under Lakehouse `Files/bronze` before applying curated transformations.

## ADR-004 — Fabric Data Factory for ingestion orchestration

**Status:** Accepted

I use Fabric pipelines and Copy activities for source ingestion so extraction can be parameterized, scheduled, monitored and chained with notebook activities.

## ADR-005 — CKAN API as the first stable ingestion source

**Status:** Accepted for the first milestone

The direct Bicing GBFS endpoint returned a temporary HTTP 503 block through Fabric. I used Barcelona Open Data CKAN to validate the first ingestion path independently of that upstream limitation.

## ADR-006 — Preserve source codes as strings in Silver

**Status:** Accepted

Numeric-looking geographic codes remain strings because they are identifiers rather than measures.

## ADR-007 — Name the first curated table by its actual grain

**Status:** Accepted

I use `silver_district_context` because the source contains multiple observations per district rather than one row per district.

## ADR-008 — Use CityBikes as the operational Bicing REST source

**Status:** Accepted

I use the CityBikes Bicing network endpoint because it exposes station-level availability through a REST response that Fabric can ingest directly.

## ADR-009 — Separate initial snapshot ingestion from historical snapshot design

**Status:** Accepted

The first Bicing payload is stored as `bicing_snapshot.json` to validate ingestion and transformation independently from the historical design.

Historical snapshot persistence will be implemented before time-based Gold analysis.

## ADR-010 — Parse Bicing timestamps explicitly

**Status:** Accepted

The source timestamp representation included both an explicit UTC offset and a trailing `Z`, which caused Spark's default timestamp conversion to return null values.

I normalize the trailing `Z` and use an explicit timestamp pattern so parsing behavior is deterministic.

## ADR-011 — Distinguish critical failures from source-quality warnings

**Status:** Accepted

Not every source inconsistency should invalidate an entire ingestion batch.

Critical issues such as missing identifiers, missing timestamps, invalid coordinates, negative availability values or duplicate station snapshots stop the Silver transformation.

The bike-type breakdown mismatch is retained as a non-critical warning because the source does not guarantee that:

```text
free_bikes = ebikes + normal_bikes
```

I preserve the source values and expose the result through `bike_breakdown_valid` instead of altering or discarding the record.
