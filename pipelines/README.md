# Fabric Pipelines

## pl_ingest_mobility_bronze

I created this Fabric Data Factory pipeline as the first ingestion layer of the platform.

### Activity

```text
cp_ingest_mobility_bronze
```

### Source configuration

| Setting | Value |
|---|---|
| Connector | REST |
| Base URL | `https://opendata-ajuntament.barcelona.cat/data/api/action/` |
| Relative URL | `datastore_search?resource_id=af254edd-7297-497e-a409-48523dd96175&limit=100` |
| Method | GET |
| Authentication | Anonymous |
| Privacy level | Public |

The source returns a CKAN JSON envelope containing metadata, field definitions and the `result.records` payload.

### Destination configuration

| Setting | Value |
|---|---|
| Destination | Fabric Lakehouse |
| Lakehouse | `barcelona_mobility_lakehouse` |
| Root | Files |
| Folder | `bronze/opendata/district_data/` |
| File | `district_data.json` |
| Format | JSON |

### Data flow

```text
Open Data Barcelona REST API
            |
            v
cp_ingest_mobility_bronze
            |
            v
OneLake / Lakehouse Files
            |
            v
bronze/opendata/district_data/district_data.json
```

## Validation completed

I verified the REST connection with Fabric data preview, confirmed a successful CKAN response and executed the pipeline until the raw JSON was materialized in the Lakehouse Bronze path.

## Troubleshooting note

I initially tested the public Bicing GBFS endpoint through the Fabric REST connector. The upstream API returned HTTP 503 with a temporary API Management block, so I kept the Bicing source out of the active pipeline and used the Barcelona Open Data CKAN API to validate the ingestion architecture without coupling the first milestone to an unstable upstream response.

## Evidence

![REST source preview](../assets/images/02-rest-source-preview.png)

![Bronze pipeline execution](../assets/images/03-bronze-pipeline-run.png)

![Bronze file in OneLake](../assets/images/04-bronze-file.png)
