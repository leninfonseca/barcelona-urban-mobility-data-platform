from pyspark.sql.functions import col, count, countDistinct, current_timestamp, explode, max, min, to_timestamp, trim, when

BRONZE_PATH = "Files/bronze/opendata/district_data/district_data.json"
SILVER_TABLE = "silver_district_context"

raw_df = (
    spark.read
    .option("multiline", "true")
    .json(BRONZE_PATH)
)

records_df = (
    raw_df
    .select(explode(col("result.records")).alias("record"))
)

districts_df = records_df.select("record.*")

silver_df = (
    districts_df
    .select(
        col("_id").cast("long").alias("source_id"),
        trim(col("AEB")).alias("aeb"),
        trim(col("Codi_Barri")).alias("neighborhood_code"),
        trim(col("Codi_Districte")).alias("district_code"),
        trim(col("Nom_Barri")).alias("neighborhood_name"),
        trim(col("Nom_Districte")).alias("district_name"),
        trim(col("Seccio_Censal")).alias("census_section"),
        trim(col("NACIONALITAT_DOMICILI")).alias("nationality_code"),
        col("Valor").cast("double").alias("value"),
        to_timestamp(col("Data_Referencia")).alias("reference_date")
    )
    .dropDuplicates()
    .withColumn("silver_processed_at", current_timestamp())
)

total_rows = silver_df.count()
unique_ids = silver_df.select("source_id").distinct().count()
duplicate_ids = total_rows - unique_ids

null_critical = silver_df.filter(
    col("source_id").isNull()
    | col("district_code").isNull()
    | col("district_name").isNull()
    | col("value").isNull()
).count()

negative_values = silver_df.filter(col("value") < 0).count()

assert total_rows > 0, "Silver table is empty"
assert duplicate_ids == 0, "Duplicate source_id values detected"
assert null_critical == 0, "Null values detected in critical columns"
assert negative_values == 0, "Negative values detected in value column"

(
    silver_df.write
    .format("delta")
    .mode("overwrite")
    .option("overwriteSchema", "true")
    .saveAsTable(SILVER_TABLE)
)

validated_df = spark.table(SILVER_TABLE)

print(f"Rows in Silver Delta table: {validated_df.count()}")

display(
    validated_df.select(
        min("value").alias("min_value"),
        max("value").alias("max_value"),
        countDistinct("district_code").alias("district_count"),
        countDistinct("neighborhood_code").alias("neighborhood_count")
    )
)

display(validated_df)
