from pyspark.sql import SparkSession, DataFrame
import pyspark.sql.functions as F
from pyspark.sql.window import Window
import zipfile

class Bai7:
    def __init__(self, spark: SparkSession):
        self.spark = spark

    def read_input(self, zip_path: str, inner_file: str) -> DataFrame:
        with zipfile.ZipFile(zip_path, 'r') as z:
            data = z.read(inner_file)
        rdd = self.spark.sparkContext.parallelize(data.decode('utf-8').splitlines())
        return self.spark.read.csv(rdd, header=True, inferSchema=True)

    def add_source_file_column(self, df: DataFrame, file_label: str) -> DataFrame:
        return df.withColumn("source_file", F.lit(file_label))

    def extract_file_date(self, df: DataFrame) -> DataFrame:
        date_pattern = r"(\d{4}-\d{2}-\d{2})"
        return df.withColumn(
            "file_date",
            F.to_date(F.regexp_extract(F.col("source_file"), date_pattern, 1), "yyyy-MM-dd")
        )

    def add_brand_column(self, df: DataFrame) -> DataFrame:
        return df.withColumn(
            "brand",
            F.when(F.col("model").contains(" "), F.split(F.col("model"), " ")[0])
             .otherwise(F.lit("unknown"))
        )

    def compute_storage_ranking(self, df: DataFrame) -> DataFrame:
        model_caps = (
            df.select("model", "capacity_bytes").distinct()
              .withColumn(
                  "storage_ranking",
                  F.dense_rank().over(Window.orderBy(F.col("capacity_bytes").desc()))
              )
        )
        return df.join(model_caps, on=["model", "capacity_bytes"], how="left")

    def add_primary_key(self, df: DataFrame) -> DataFrame:
        cols_to_hash = [c for c in df.columns if c != "primary_key"]
        return df.withColumn("primary_key", F.sha2(F.concat_ws("||", *cols_to_hash), 256))

    def transform(self, df: DataFrame, file_label: str) -> DataFrame:
        df = self.add_source_file_column(df, file_label)
        df = self.extract_file_date(df)
        df = self.add_brand_column(df)
        df = self.compute_storage_ranking(df)

        df = df.dropDuplicates([
            "file_date", "source_file", "brand", "capacity_bytes", "storage_ranking"
        ])

        df = self.add_primary_key(df)
        return df


def main():
    spark = SparkSession.builder.appName("Exercise7_OOP").enableHiveSupport().getOrCreate()

    processor = Bai7(spark)

    zip_path = "/app/data/hard-drive-2022-01-01-failures.csv.zip"
    inner_file = "hard-drive-2022-01-01-failures.csv"

    df = processor.read_input(zip_path, inner_file)
    result = processor.transform(df, inner_file)

    result.select(
        "file_date", "source_file", "brand", "capacity_bytes", "storage_ranking", "primary_key"
    ).show(20, truncate=False)


if __name__ == "__main__":
    main()