from pyspark.sql import SparkSession
import pandas as pd
from pyspark.sql import functions as f

from transactionAnalysis import *


def read_in_data(user):
    # TODO update path to jar location on machine/ password for db
    # pathJar = "/Users/allison/Drivers/postgresql-42.3.4.jar"
    # if user:
    #     pathJar = "TODO: hiba path"

    spark = SparkSession \
        .builder \
        .appName("Coffee Sales") \
        .config("spark.jars", "/opt/spark/jars") \
        .getOrCreate()
    spark.conf.set("spark.sql.repl.eagerEval.enabled", True)

    df = spark.read \
        .format("jdbc") \
        .option("url", "jdbc:postgresql://127.0.0.1:5432/dse6300") \
        .option("dbtable", "sale_transactions") \
        .option("user", "postgres") \
        .option("password", "pass1234") \
        .option("driver", "org.postgresql.Driver") \
        .load()
    # TODO Hiba change the path string below to that of the csv on your local machine
    # until we fix your db issues
    # df = spark.read.csv('/content/authors.csv', sep=',',
    #                          inferSchema=True, header=True)

    df = df.where(df.transaction_id != 'transaction_id')
    df.describe().toPandas().transpose()
    df = df.withColumn("quantity", df.quantity.cast("Float"))
    df = df.withColumn("unit_price", df.unit_price.cast("Float"))
    df = df.withColumn("line_item_amount", df.line_item_amount.cast("Float"))
    df = df.withColumn("transaction_date_time",
                       f.concat(df.transaction_date, f.lit(" "), df.transaction_time))
    df = df.withColumn('transaction_date_time', f.from_unixtime(f.unix_timestamp('transaction_date_time',
                                                                                 'yyyy-MM-dd HH:mm:ss')))
    df = df.dropna(how='any')
    df = df.dropDuplicates()
    df.printSchema()
    return df


if __name__ == '__main__':
    data = read_in_data(False)
    # Uncomment/ comment out algorithm to run
    run_fp_growth(data)
    # plotLineItemAmount(data)
