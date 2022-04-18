from pyspark.sql import functions as f
from pyspark.ml.fpm import FPGrowth
import matplotlib.pyplot as plt
import numpy as np

def run_fp_growth(sales_df):
    sales_df = sales_df.groupby("transaction_date_time", "sales_outlet_id", "transaction_id", "staff_id", "line_item_id",
                                "order")\
        .agg(f.collect_list("product_id")).sort("transaction_date_time", "sales_outlet_id", "transaction_id", "staff_id",
                                                "line_item_id", "order")
    # Frequent Pattern Growth – FP Growth is a method of mining frequent itemsets using support, lift, and confidence.
    fpGrowth = FPGrowth(itemsCol="collect_list(product_id)", minSupport=0.006, minConfidence=0.006)
    model = fpGrowth.fit(sales_df)
    # Display frequent itemsets.
    model.freqItemsets.show()
    items = model.freqItemsets
    # Display generated association rules.
    model.associationRules.show()
    rules = model.associationRules
    # transform examines the input items against all the association rules and summarize the consequents as prediction
    model.transform(sales_df).show()
    transformed = model.transform(sales_df)


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
