import argparse
import os
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, avg, sum as spark_sum, count


def main():

    parser = argparse.ArgumentParser()

    parser.add_argument("--input", type=str, required=True)

    parser.add_argument("--output", type=str, required=True)

    args = parser.parse_args()

    spark = (
        SparkSession.builder
        .appName("CoffeeSalesPipeline")
        .master("local[*]")
        .getOrCreate()
    )

    spark.sparkContext.setLogLevel("WARN")

    input_file = os.path.join(args.input, "coffee_sales.csv")

    df = spark.read.csv(input_file, header=True, inferSchema=True)

    # Feature engineering
    df = df.withColumn("total_sale", col("price") * col("quantity"))

    # Aggregation: drink popularity
    drink_popularity = (
        df.groupBy("drink")
        .agg(
            count("*").alias("orders"),
            spark_sum("quantity").alias("total_quantity"),
            avg("price").alias("avg_price")
        )
    )

    # Aggregation: sales per store
    cafe_sales = (
        df.groupBy("store")
        .agg(
            spark_sum("total_sale").alias("total_revenue"),
            count("*").alias("orders")
        )
    )

    os.makedirs(args.output, exist_ok=True)

    drink_popularity.write.mode("overwrite").csv(
        os.path.join(args.output, "drink_popularity"), header=True
    )

    cafe_sales.write.mode("overwrite").csv(
        os.path.join(args.output, "cafe_sales"), header=True
    )

    print("Pipeline completed successfully")

    spark.stop()


if __name__ == "__main__":
    main()
