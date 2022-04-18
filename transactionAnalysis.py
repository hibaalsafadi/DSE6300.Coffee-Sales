from pyspark.sql import functions as f


def run_retail_analysis(sales_df):
    # sales_df.groupby("transaction_date_time").count().sort("transaction_date_time", ascending=True).limit(10).show()
    sales_df.show()
