from pyspark.sql import functions as f
from kafka import KafkaProducer
from pyspark.ml.fpm import FPGrowth
import matplotlib.pyplot as plt
import numpy as np
import json


def createProducer():
    producer = KafkaProducer(
        bootstrap_servers='kafka:9092',
        value_serializer=lambda v: json.dumps(v).encode('utf-8'))
    return producer


def run_fp_growth(sales_df):
    sales_df = sales_df.groupby("transaction_date_time", "sales_outlet_id", "transaction_id", "staff_id", "line_item_id"
                                , "order")\
        .agg(f.collect_list("product_id")).sort("transaction_date_time", "sales_outlet_id", "transaction_id", "staff_id",
                                                "line_item_id", "order")
    # Frequent Pattern Growth – FP Growth is a method of mining frequent itemsets using support, lift, and confidence.
    fpGrowth = FPGrowth(itemsCol="collect_list(product_id)", minSupport=0.015, minConfidence=0.001)
    model = fpGrowth.fit(sales_df)
    # Display frequent itemsets.
    items = model.freqItemsets.toPandas()
    items.sort_values(by=['freq'], ascending=False)
    print(items.head(20))
    producer = createProducer()
    producer.send('results', items.to_json())
    model.transform(sales_df).show()


def plotLineItemAmount(data_df):
    results = data_df.groupby("transaction_date").sum().sort("transaction_date")
    dates = range(1, 30)
    values = np.array(results.select("sum(line_item_amount)").collect()).reshape(-1)
    plt.bar(dates, values)
    plt.xticks(dates, rotation=45)
    labels, location = plt.yticks()
    plt.yticks(labels, (labels/1000).astype(int))
    plt.ylabel('Sales in thousands USD')
    plt.title('Coffee Product Sales for April 2019')
    plt.xlabel('Date')
    plt.show()
