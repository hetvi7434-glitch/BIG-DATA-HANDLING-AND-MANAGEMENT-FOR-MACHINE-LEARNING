import os
import sys
import pyspark

# Configure Spark, Python & Java paths explicitly to prevent gateway launch failures
spark_home = os.path.dirname(pyspark.__file__)
os.environ["SPARK_HOME"] = spark_home
os.environ["SPARK_SCALA_VERSION"] = "2.13"
os.environ["PYSPARK_PYTHON"] = sys.executable
os.environ["PYSPARK_DRIVER_PYTHON"] = sys.executable
os.environ["SPARK_LOCAL_IP"] = "127.0.0.1"

# Resolve and validate JAVA_HOME (clean trailing slashes)
java_candidates = [
    os.environ.get("JAVA_HOME", "").rstrip("/\\"),
    r"C:\Program Files\Microsoft\jdk-17.0.20.101-hotspot",
    os.path.expanduser(r"~\AppData\Local\Java\jdk-17")
]
for jc in java_candidates:
    if jc and os.path.isfile(os.path.join(jc, "bin", "java.exe")):
        os.environ["JAVA_HOME"] = jc
        os.environ["PATH"] = os.path.join(jc, "bin") + os.pathsep + os.environ.get("PATH", "")
        break

# Resolve Hadoop winutils for Windows support
hadoop_candidates = [
    os.environ.get("HADOOP_HOME", "").rstrip("/\\"),
    os.path.expanduser(r"~\AppData\Local\hadoop")
]
for hc in hadoop_candidates:
    if hc and os.path.isdir(hc):
        os.environ["HADOOP_HOME"] = hc
        os.environ["PATH"] = os.path.join(hc, "bin") + os.pathsep + os.environ.get("PATH", "")
        break

from pyspark.sql import SparkSession
from pyspark.sql.functions import col

spark = SparkSession.builder.appName("DS505_Transformations").master("local[*]").getOrCreate()

# Create sample dataset
data = [
    (1, "Aarav", "IT", 65000, "Surat"),
    (2, "Diya", "HR", 45000, "Navsari"),
    (3, "Rohan", "IT", 72000, "Surat"),
    (4, "Pooja", "Finance", 58000, "Ahmedabad"),
    (5, "Kabir", "IT", 81000, "Surat"),
    (6, "Neha", "Finance", 62000, "Surat")
]
columns = ["ID", "Name", "Dept", "Salary", "City"]
df = spark.createDataFrame(data, columns)

print("--- ORIGINAL DATAFRAME ---")
df.show()

# 1. Column Selection
print("--- 1. SELECT NAME AND SALARY ---")
df.select("Name", "Salary").show()

# 2. Multi-condition Filtering
print("--- 2. FILTER (Dept == 'IT' AND Salary > 70000) ---")
df.filter((col("Dept") == "IT") & (col("Salary") > 70000)).show()

# 3. Add Computed Column (Bonus = 10% of Salary)
print("--- 3. ADD COMPUTED 'Bonus' COLUMN ---")
df_with_bonus = df.withColumn("Bonus", col("Salary") * 0.10)
df_with_bonus.show()

# 4. Rename Column
print("--- 4. RENAME 'Salary' TO 'Base_Salary' ---")
df_renamed = df_with_bonus.withColumnRenamed("Salary", "Base_Salary")
df_renamed.show()

# Stop SparkSession cleanly to release background Java worker processes
spark.stop()
