# Data Model

I evolve the model layer by layer after inspecting the real source structures.

## Bronze

Current raw objects:

```text
Files/bronze/opendata/district_data/district_data.json
Files/bronze/citybikes/bicing/bicing_snapshot.json
```

### Context source

The CKAN response contains:

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

### Bicing source

The CityBikes response contains:

```text
root
└── network
    ├── id
    ├── name
    ├── location
    ├── company
    ├── ebikes
    └── stations
        ├── id
        ├── name
        ├── latitude
        ├── longitude
        ├── timestamp
        ├── free_bikes
        ├── empty_slots
        └── extra
```

I keep both source envelopes intact in Bronze.

## Silver

### silver_district_context

The first curated table is operational.

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

### silver_bicing_station_status

This table is the next implementation target.

The intended grain is **one Bicing station observation per source snapshot**.

Candidate fields, subject to schema validation in PySpark, include:

- station_id
- station_name
- latitude
- longitude
- source_timestamp
- free_bikes
- empty_slots
- operational attributes from `extra`
- silver_processed_at

I will finalize types and accepted ranges only after inspecting the actual Spark schema.

## Gold

I will define the Gold model after the Bicing Silver table is operational and historical snapshot behavior is established.
