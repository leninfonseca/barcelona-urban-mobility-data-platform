# Data Model

I evolve the model layer by layer after inspecting the real source structures.

## Bronze

Current raw objects:

```text
Files/bronze/opendata/district_data/district_data.json
Files/bronze/citybikes/bicing/bicing_snapshot.json
```

## Silver

### silver_district_context

This contextual table is operational and contains typed geographic and demographic observations.

### silver_bicing_station_status

This station-level Delta table is now operational.

**Grain:** one Bicing station observation per source timestamp.

Current columns:

| Column | Type | Purpose |
|---|---|---|
| station_id | string | CityBikes station identifier |
| station_uid | long | Bicing station UID exposed by the source |
| station_name | string | Station name/location label |
| latitude | double | Station latitude |
| longitude | double | Station longitude |
| source_timestamp | timestamp | Timestamp reported by the source |
| free_bikes | long | Available bikes |
| empty_slots | long | Available docking slots |
| ebikes | long | Available electric bikes |
| normal_bikes | long | Available standard bikes |
| has_ebikes | boolean | Source capability flag |
| is_online | boolean | Source station status |
| station_capacity | long | Derived as free bikes + empty slots |
| bike_breakdown_valid | boolean | Quality flag for bike-type consistency |
| silver_processed_at | timestamp | Silver processing timestamp |

The current validated table contains 544 station observations.

The pair `station_id + source_timestamp` defines the snapshot-level uniqueness rule used during deduplication and quality validation.

## Gold

The Gold model will be defined after historical Bicing snapshots are preserved and incremental processing is implemented. This avoids designing time-based facts before the historical grain is established.
