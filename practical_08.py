import os
import sys
import urllib.request

# ----------------- WINDOWS HADOOP / WINUTILS AUTO-FIX -----------------
if sys.platform.startswith("win"):
    hadoop_dir = r"C:\hadoop"
    hadoop_bin = os.path.join(hadoop_dir, "bin")
    winutils_exe = os.path.join(hadoop_bin, "winutils.exe")
    hadoop_dll = os.path.join(hadoop_bin, "hadoop.dll")

    if not os.path.isfile(winutils_exe):
        try:
            print("Configuring Hadoop winutils for Windows...")
            os.makedirs(hadoop_bin, exist_ok=True)
            urllib.request.urlretrieve(
                "https://raw.githubusercontent.com/cdarlint/winutils/master/hadoop-3.3.6/bin/winutils.exe",
                winutils_exe
            )
            urllib.request.urlretrieve(
                "https://raw.githubusercontent.com/cdarlint/winutils/master/hadoop-3.3.6/bin/hadoop.dll",
                hadoop_dll
            )
            print("Hadoop winutils configured successfully.")
        except Exception as e:
            print(f"Warning: Could not download winutils: {e}")

    os.environ["HADOOP_HOME"] = hadoop_dir
    os.environ["PATH"] = hadoop_bin + os.pathsep + os.environ.get("PATH", "")

os.environ["PYSPARK_PYTHON"] = sys.executable
os.environ["PYSPARK_DRIVER_PYTHON"] = sys.executable
# ----------------------------------------------------------------------

from pyspark.sql import SparkSession

# Initialize SparkSession
spark = SparkSession.builder \
    .appName("DS505_Parquet") \
    .master("local[*]") \
    .config("spark.sql.warehouse.dir", os.path.abspath("spark-warehouse")) \
    .getOrCreate()

# Suppress verbose JVM INFO logs
spark.sparkContext.setLogLevel("WARN")

# Step 1: Create sample IoT sensor telemetry DataFrame
data = [
    ("Sensor_01", "Temperature", 24.5, "2026-10-10 10:00:00"),
    ("Sensor_02", "Humidity", 65.2, "2026-10-10 10:00:00"),
    ("Sensor_01", "Temperature", 25.1, "2026-10-10 10:05:00"),
    ("Sensor_03", "Pressure", 1013.25, "2026-10-10 10:05:00"),
    ("Sensor_02", "Humidity", 64.8, "2026-10-10 10:10:00")
]
columns = ["Sensor_ID", "Metric_Type", "Metric_Value", "Timestamp"]

df = spark.createDataFrame(data, columns)

print("\n--- ORIGINAL SENSOR DATAFRAME ---")
df.show()

# Step 2: Write to Apache Parquet columnar file format
parquet_path = "sensor_telemetry.parquet"
df.write.mode("overwrite").parquet(parquet_path)
print(f"\nSuccessfully serialized DataFrame to Parquet storage at: '{parquet_path}'")

# Step 3: Read back from Parquet format
df_parquet = spark.read.parquet(parquet_path)

print("\n--- RELOADED FROM PARQUET FORMAT ---")
df_parquet.printSchema()
df_parquet.show()

print(f"Verified Record Count: {df_parquet.count()} rows.")

# Stop SparkSession cleanly
spark.stop()
