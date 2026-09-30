# Data Model

I am evolving the model layer by layer instead of defining the final schema before inspecting the real sources.

## Bronze

Current raw object:

```text
Files/bronze/opendata/district_data/district_data.json
```

The CKAN response contains this high-level structure:

```text
root
├── help
├── success
└── result
    ├── resource_id
    ├── fields
    ├── records
    └── ...
```

I keep this envelope intact in Bronze so source metadata and raw records remain reproducible.

## Silver

The first curated table is:

```text
silver_district_context
```

Its grain is contextual demographic/geographic observation by source record, not one row per district.

Current columns:

| Column | Type | Purpose |
|---|---|---|
| source_id | long | Source record identifier |
| aeb | string | AEB code |
| neighborhood_code | string | Neighborhood identifier |
| district_code | string | District identifier |
| neighborhood_name | string | Neighborhood name |
| district_name | string | District name |
| census_section | string | Census section identifier |
| nationality_code | string | Source nationality category |
| value | double | Observed numeric value |
| reference_date | timestamp | Source reference timestamp |
| silver_processed_at | timestamp | Silver processing timestamp |

Geographic and categorical codes are stored as strings because they are identifiers rather than measures.

The initial transformation preserved all 100 records retrieved from the source sample and removed no valid rows.

## Gold

I will define the Gold model after mobility-specific sources are available and the common analytical grain is clear. Candidate entities include date, location, transport/mobility source and mobility observations.
