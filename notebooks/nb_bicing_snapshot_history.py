from pyspark.sql.functions import (
    col,
    current_timestamp,
    explode,
    input_file_name,
    max as spark_max,
    regexp_extract,
    regexp_replace,
    to_timestamp,
    trim,
)
from delta.tables import DeltaTable
import re
from datetime import datetime

HISTORY_ROOT = "Files/bronze/citybikes/bicing/history"
HISTORY_TABLE = "silver_bicing_station_history"

table_exists = spark.catalog.tableExists(HISTORY_TABLE)

if table_exists:
    watermark = (
        spark.table(HISTORY_TABLE)
        .agg(spark_max("snapshot_ingested_at").alias("watermark"))
        .first()["watermark"]
    )
    print(f"Historical Silver table found: {HISTORY_TABLE}")
    print(f"Current watermark: {watermark}")
else:
    watermark = None
    print(f"Historical Silver table not found: {HISTORY_TABLE}")
    print("Bootstrap mode enabled. All available Bronze snapshots will be processed.")

def list_files_recursive(path):
    files = []
    for item in notebookutils.fs.ls(path):
        if item.isDir:
            files.extend(list_files_recursive(item.path))
        else:
            files.append(item.path)
    return files

all_snapshot_files = list_files_recursive(HISTORY_ROOT)
snapshot_pattern = re.compile(r"bicing_(\d{8}_\d{6})\.json$")
new_snapshot_files = []

for file_path in all_snapshot_files:
    match = snapshot_pattern.search(file_path)
    if match:
        snapshot_datetime = datetime.strptime(match.group(1), "%Y%m%d_%H%M%S")
        if watermark is None or snapshot_datetime > watermark:
            new_snapshot_files.append(file_path)

print(f"Snapshot files found: {len(all_snapshot_files)}")
print(f"New snapshots after watermark: {len(new_snapshot_files)}")

if len(new_snapshot_files) == 0:
    print("No new snapshots to process. Silver history is already up to date.")
    notebookutils.notebook.exit("No new snapshots to process.")

print(f"{len(new_snapshot_files)} new snapshot(s) will be processed.")

incremental_raw_df = (
    spark.read
    .option("multiline", "true")
    .json(new_snapshot_files)
    .withColumn("source_file", input_file_name())
)

incremental_stations_df = (
    incremental_raw_df
    .select(
        "source_file",
        explode(col("network.stations")).alias("station"),
    )
    .withColumn(
        "snapshot_text",
        regexp_extract(
            col("source_file"),
            r"bicing_(\d{8}_\d{6})\.json$",
            1,
        ),
    )
    .withColumn(
        "snapshot_ingested_at",
        to_timestamp(col("snapshot_text"), "yyyyMMdd_HHmmss"),
    )
    .select(
        "source_file",
        "snapshot_ingested_at",
        "station.*",
    )
)

incremental_silver_df = (
    incremental_stations_df
    .select(
        col("id").alias("station_id"),
        col("extra.uid").cast("long").alias("station_uid"),
        trim(col("name")).alias("station_name"),
        col("latitude").cast("double").alias("latitude"),
        col("longitude").cast("double").alias("longitude"),
        col("snapshot_ingested_at"),
        to_timestamp(
            regexp_replace(col("timestamp"), "Z$", ""),
            "yyyy-MM-dd'T'HH:mm:ss.SSSSSSXXX",
        ).alias("source_timestamp"),
        col("free_bikes").cast("long").alias("free_bikes"),
        col("empty_slots").cast("long").alias("empty_slots"),
        col("extra.ebikes").cast("long").alias("ebikes"),
        col("extra.normal_bikes").cast("long").alias("normal_bikes"),
        col("extra.has_ebikes").cast("boolean").alias("has_ebikes"),
        col("extra.online").cast("boolean").alias("is_online"),
        col("source_file"),
    )
    .withColumn("station_capacity", col("free_bikes") + col("empty_slots"))
    .withColumn(
        "bike_breakdown_valid",
        col("free_bikes") == (col("ebikes") + col("normal_bikes")),
    )
    .withColumn("silver_processed_at", current_timestamp())
    .dropDuplicates(["station_id", "snapshot_ingested_at"])
)

incremental_rows = incremental_silver_df.count()
incremental_duplicates = (
    incremental_silver_df
    .groupBy("station_id", "snapshot_ingested_at")
    .count()
    .filter(col("count") > 1)
    .count()
)
incremental_null_critical = (
    incremental_silver_df
    .filter(
        col("station_id").isNull()
        | col("snapshot_ingested_at").isNull()
        | col("source_timestamp").isNull()
        | col("latitude").isNull()
        | col("longitude").isNull()
    )
    .count()
)
incremental_null_availability = (
    incremental_silver_df
    .filter(
        col("free_bikes").isNull()
        | col("empty_slots").isNull()
        | col("ebikes").isNull()
        | col("normal_bikes").isNull()
    )
    .count()
)
incremental_invalid_availability = (
    incremental_silver_df
    .filter(
        (col("free_bikes") < 0)
        | (col("empty_slots") < 0)
        | (col("ebikes") < 0)
        | (col("normal_bikes") < 0)
    )
    .count()
)
incremental_invalid_coordinates = (
    incremental_silver_df
    .filter(
        (col("latitude") < -90)
        | (col("latitude") > 90)
        | (col("longitude") < -180)
        | (col("longitude") > 180)
    )
    .count()
)
incremental_warnings = (
    incremental_silver_df
    .filter(col("bike_breakdown_valid") == False)
    .count()
)

assert incremental_rows > 0, "Incremental batch is empty"
assert incremental_duplicates == 0, "Duplicate incremental observations detected"
assert incremental_null_critical == 0, "Critical nulls detected in incremental batch"
assert incremental_null_availability == 0, "Availability nulls detected in incremental batch"
assert incremental_invalid_availability == 0, "Invalid availability values detected"
assert incremental_invalid_coordinates == 0, "Invalid station coordinates detected"

if incremental_warnings > 0:
    print(
        f"WARNING: {incremental_warnings} incremental records "
        "have an inconsistent bike breakdown."
    )

print("All critical incremental data quality checks passed.")

if not spark.catalog.tableExists(HISTORY_TABLE):
    (
        incremental_silver_df.limit(0)
        .write
        .format("delta")
        .saveAsTable(HISTORY_TABLE)
    )

target_delta = DeltaTable.forName(spark, HISTORY_TABLE)
rows_before = spark.table(HISTORY_TABLE).count()

(
    target_delta.alias("target")
    .merge(
        incremental_silver_df.alias("source"),
        """
        target.station_id = source.station_id
        AND target.snapshot_ingested_at = source.snapshot_ingested_at
        """,
    )
    .whenNotMatchedInsertAll()
    .execute()
)

rows_after = spark.table(HISTORY_TABLE).count()
rows_inserted = rows_after - rows_before

print(f"Rows before MERGE: {rows_before}")
print(f"Rows after MERGE: {rows_after}")
print(f"Rows inserted: {rows_inserted}")

history_df = spark.table(HISTORY_TABLE)
history_duplicates = (
    history_df
    .groupBy("station_id", "snapshot_ingested_at")
    .count()
    .filter(col("count") > 1)
    .count()
)
new_watermark = (
    history_df
    .agg(spark_max("snapshot_ingested_at").alias("watermark"))
    .first()["watermark"]
)

print(f"Historical Silver rows: {history_df.count()}")
print(
    "Historical snapshots: "
    f"{history_df.select('snapshot_ingested_at').distinct().count()}"
)
print(f"Duplicate historical observations: {history_duplicates}")
print(f"Previous watermark: {watermark}")
print(f"New watermark: {new_watermark}")

assert history_duplicates == 0, "Duplicate observations detected after MERGE"

if watermark is not None and rows_inserted > 0:
    assert new_watermark > watermark, "Watermark did not advance after inserting new data"

print("Historical Silver validation completed successfully.")
