# Engineering Decisions

This document records important architectural and implementation decisions.

## ADR-001 — Medallion architecture

**Status:** Accepted

The platform uses Bronze, Silver and Gold layers to separate raw ingestion, validated/transformed data and analytical data products.

## ADR-002 — Delta tables

**Status:** Accepted

Delta tables will be used in the Fabric Lakehouse to support reliable table operations and future incremental/upsert patterns.

Further decisions will be added as the project evolves.
