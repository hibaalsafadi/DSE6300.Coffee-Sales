from pyspark.sql import SparkSession
from kafka import KafkaProducer
from transactionAnalysis import *
from ApiriorAlgorithim import *
import pandas as pd
import json


def createProducer():
    producer = KafkaProducer(
        bootstrap_servers='kafka:9092',
        value_serializer=lambda v: json.dumps(v).encode('utf-8'))
    return producer


def read_in_data():
    spark = SparkSession \
        .builder \
        .appName("Coffee Sales") \
        .config("spark.jars", "/opt/spark/jars") \
        .getOrCreate()
    spark.conf.set("spark.sql.repl.eagerEval.enabled", True)

    df = spark.read \
        .format("jdbc") \
        .option("url", "jdbc:postgresql://host.docker.internal:5432/dse6300") \
        .option("dbtable", "sale_transactions") \
        .option("user", "postgres") \
        .option("password", "pass1234") \
        .option("driver", "org.postgresql.Driver") \
        .load()

    df = df.where(df.transaction_id != 'transaction_id')
    df = df.withColumn("quantity", df.quantity.cast("Float"))
    df = df.withColumn("unit_price", df.unit_price.cast("Float"))
    df = df.withColumn("line_item_amount", df.line_item_amount.cast("Float"))
    df = df.withColumn("transaction_date_time",
                       f.concat(df.transaction_date, f.lit(" "), df.transaction_time))
    df = df.withColumn('transaction_date_time', f.from_unixtime(f.unix_timestamp('transaction_date_time',
                                                                                 'yyyy-MM-dd HH:mm:ss')))
    df = df.dropna(how='any')
    df = df.dropDuplicates()
    pd.set_option('max_columns', None)
    df.printSchema()
    print(df.describe().toPandas().transpose())
    # print(df.toPandas().corr())
    return df


if __name__ == '__main__':
    data = read_in_data()
    producer = createProducer()
    # Uncomment/ comment out algorithm to run
    # run_fp_growth(data, producer)
    # plotLineItemAmount(data)
    # SR(data, producer)