#!/usr/bin/env python3
"""
Spark Load Test - Simulates a single student session
This script performs various Spark operations with random delays to simulate
a student working through the workshop at their own pace.
"""

import os
import sys
import time
import random
import uuid
from datetime import datetime
from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pyspark.sql.types import StringType, FloatType

# Configuration
SPARK_MASTER = os.getenv('SPARK_MASTER', 'spark://spark-master:7077')
STUDENT_ID = os.getenv('STUDENT_ID', f'student-{uuid.uuid4().hex[:8]}')
RANDOM_SEED = hash(STUDENT_ID) % 10000  # Deterministic randomness per student

# Set random seed for reproducible but varied behavior
random.seed(RANDOM_SEED)

def log(message):
    """Print timestamped log message"""
    timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]
    print(f"[{timestamp}] [{STUDENT_ID}] {message}", flush=True)

def random_delay(min_seconds=1, max_seconds=5):
    """Random delay to simulate thinking/typing time"""
    delay = random.uniform(min_seconds, max_seconds)
    time.sleep(delay)
    return delay

def create_spark_session():
    """Create Spark session with random app name"""
    app_name = f"{STUDENT_ID}-{uuid.uuid4().hex[:8]}"
    log(f"Creating Spark session: {app_name}")
    
    spark = SparkSession.builder \
        .appName(app_name) \
        .master(SPARK_MASTER) \
        .config('spark.executor.cores', '1') \
        .config('spark.executor.memory', '500m') \
        .config('spark.driver.memory', '256m') \
        .config('spark.cores.max', '1') \
        .config('spark.default.parallelism', '1') \
        .config('spark.sql.shuffle.partitions', '1') \
        .config('spark.dynamicAllocation.enabled', 'false') \
        .getOrCreate()
    
    log(f"Spark session created successfully")
    return spark

def exercise_1_read_data(spark):
    """Exercise 1: Read CSV files"""
    log("=== Exercise 1: Reading CSV files ===")
    
    # Try different paths (students might use different paths)
    paths = [
        "/data/csv/beers.csv",
        "/datasets/csv/beers.csv",
        "/opt/spark-data/csv/beers.csv"
    ]
    
    beers_path = None
    breweries_path = None
    
    for base_path in paths:
        test_beers = base_path
        test_breweries = base_path.replace('beers.csv', 'breweries.csv')
        try:
            # Test if file exists by trying to read schema
            df_test = spark.read.csv(test_beers, header=True)
            df_test.schema  # Trigger lazy evaluation
            beers_path = test_beers
            breweries_path = test_breweries
            log(f"Found data at: {base_path}")
            break
        except Exception as e:
            continue
    
    if not beers_path:
        log("ERROR: Could not find CSV files")
        return None, None
    
    random_delay(0.5, 2.0)
    df_beers = spark.read.csv(beers_path, header=True)
    log(f"Read beers.csv: {df_beers.count()} rows")
    
    random_delay(0.5, 2.0)
    df_breweries = spark.read.csv(breweries_path, header=True)
    log(f"Read breweries.csv: {df_breweries.count()} rows")
    
    return df_beers, df_breweries

def exercise_2_simple_operations(spark, df_beers):
    """Exercise 2: Simple DataFrame operations"""
    log("=== Exercise 2: Simple operations ===")
    
    random_delay(1, 3)
    
    # Count operation
    count = df_beers.count()
    log(f"Total beers: {count}")
    
    random_delay(1, 2)
    
    # Show sample
    df_beers.select("name", "abv").limit(5).show(truncate=False)
    
    random_delay(1, 3)
    
    # Simple filter
    filtered = df_beers.filter(F.col("abv").isNotNull()).count()
    log(f"Beers with ABV: {filtered}")

def exercise_3_udf_operations(spark, df_beers):
    """Exercise 3: UDF operations"""
    log("=== Exercise 3: UDF operations ===")
    
    random_delay(1, 4)
    
    @F.udf(returnType=StringType())
    def reverse_name(name: str):
        if name:
            return name[::-1].upper()
        return ""
    
    result = df_beers \
        .withColumn("reverse_name", reverse_name(F.col("name"))) \
        .select("name", "reverse_name") \
        .limit(10)
    
    result.show(truncate=False)
    log("UDF operation completed")

def exercise_4_joins_and_aggregations(spark, df_beers, df_breweries):
    """Exercise 4: Joins and aggregations"""
    log("=== Exercise 4: Joins and aggregations ===")
    
    random_delay(2, 5)
    
    # Join operation
    joined = df_beers.join(
        df_breweries.withColumnRenamed("name", "brewer_name"),
        on=df_beers.brewery_id == df_breweries.id
    )
    
    log("Join completed")
    
    random_delay(1, 3)
    
    # Group by country
    country_counts = joined \
        .groupby("country") \
        .count() \
        .sort(F.col("count").desc()) \
        .limit(10)
    
    country_counts.show(truncate=False)
    log("Aggregation completed")

def exercise_5_caching_and_complex_queries(spark, df_beers, df_breweries):
    """Exercise 5: Caching and complex queries"""
    log("=== Exercise 5: Caching and complex queries ===")
    
    random_delay(2, 4)
    
    # Create joined dataframe and cache it
    df_beers_brewers = df_beers.join(
        df_breweries.withColumnRenamed("name", "brewer_name"),
        on=df_beers.brewery_id == df_breweries.id
    ).cache()
    
    log("DataFrame cached")
    
    random_delay(1, 2)
    
    # Filter by country
    @F.udf(returnType=FloatType())
    def safe_float(value: str):
        try:
            return float(value) if value else 0.0
        except:
            return 0.0
    
    countries = ["France", "United States", "Belgium", "Germany"]
    selected_country = random.choice(countries)
    
    filtered = df_beers_brewers \
        .filter(F.col("country") == F.lit(selected_country)) \
        .withColumn("abv_float", safe_float(F.col("abv"))) \
        .filter(F.col("abv_float") > 0) \
        .sort(F.col("abv_float").desc()) \
        .limit(5)
    
    filtered.show(truncate=False)
    log(f"Filtered by country: {selected_country}")
    
    random_delay(1, 3)
    
    # Another operation using cached data
    avg_abv = df_beers_brewers \
        .withColumn("abv_float", safe_float(F.col("abv"))) \
        .filter(F.col("abv_float") > 0) \
        .agg(F.avg("abv_float").alias("avg_abv")) \
        .first()[0]
    
    log(f"Average ABV: {avg_abv:.2f}")
    
    # Unpersist
    df_beers_brewers.unpersist()
    log("Cache cleared")

def exercise_6_multiple_reads(spark):
    """Exercise 6: Read multiple files"""
    log("=== Exercise 6: Reading multiple files ===")
    
    random_delay(1, 3)
    
    try:
        df_styles = spark.read.csv("/datasets/csv/styles.csv", header=True)
        style_count = df_styles.count()
        log(f"Read styles.csv: {style_count} rows")
        
        random_delay(1, 2)
        
        # Simple query on styles
        df_styles.select("style_name").distinct().limit(10).show(truncate=False)
        
    except Exception as e:
        log(f"Could not read styles.csv: {e}")

def main():
    """Main execution - simulates a student session"""
    log("=" * 60)
    log(f"Starting student simulation: {STUDENT_ID}")
    log("=" * 60)
    
    try:
        # Create Spark session
        spark = create_spark_session()
        random_delay(1, 2)
        
        # Exercise 1: Read data
        df_beers, df_breweries = exercise_1_read_data(spark)
        if df_beers is None:
            log("ERROR: Failed to read data files")
            return 1
        
        random_delay(2, 5)  # Thinking time between exercises
        
        # Exercise 2: Simple operations
        exercise_2_simple_operations(spark, df_beers)
        random_delay(2, 5)
        
        # Exercise 3: UDF operations
        exercise_3_udf_operations(spark, df_beers)
        random_delay(2, 5)
        
        # Exercise 4: Joins and aggregations
        exercise_4_joins_and_aggregations(spark, df_beers, df_breweries)
        random_delay(3, 6)
        
        # Exercise 5: Caching and complex queries
        exercise_5_caching_and_complex_queries(spark, df_beers, df_breweries)
        random_delay(2, 4)
        
        # Exercise 6: Multiple reads
        exercise_6_multiple_reads(spark)
        random_delay(1, 3)
        
        # Final delay before closing
        random_delay(2, 4)
        
        log("=" * 60)
        log("Student simulation completed successfully")
        log("=" * 60)
        
        # Stop Spark session
        spark.stop()
        return 0
        
    except Exception as e:
        log(f"ERROR: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(main())
