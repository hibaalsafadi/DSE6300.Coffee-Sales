import numpy as np
import pandas as pd
from mlxtend.frequent_patterns import apriori, association_rules

# Changing the working location to the location of the file
#cd /Users/hibaalsafadi/Desktop/ApiriorAlgorithim

def hot_encode(x):
    if (x <= 0):
        return 0
    if (x >= 1):
        return 1

def SR(df):
    #Loading product data
    # df = pd.read_csv('.csv')
    # print(df.head(6))
    #
    # #Exploring the column of the product
    # print(product.columns)

    #Exploring the different regions of transactions

    df.show()


    df = df.toPandas()
    corM = df.corr()
    print(corM)
    # test_df= df.groupby(['transaction_id', 'product_id'])['quantity'].sum()
    # print(test_df.head(20))
    # # Transactions done in staff ID

    basket_3 = (df[df['sales_outlet_id'] == 3]
                .groupby(['transaction_id', 'product_id'])['quantity']
                .sum().unstack().reset_index().fillna(0)
                .set_index('transaction_id'))
    print(type(basket_3))
    print(basket_3.head(20))
    basket_encoded = basket_3.applymap(hot_encode)
    basket_3 = basket_encoded
    frq_items = apriori(basket_3, min_support=0.01, use_colnames=True)
    rules = association_rules(frq_items, metric="lift", min_threshold=1)
    rules = rules.sort_values(['confidence', 'lift'], ascending=[False, False])
    print(rules.head())
    print(frq_items.head())

    basket_5 = (df[df['sales_outlet_id'] == 5]
                .groupby(['transaction_id', 'product_id'])['quantity']
                .sum().unstack().reset_index().fillna(0)
                .set_index('transaction_id'))
    print(type(basket_5))
    print(basket_5.head(20))
    basket_encoded = basket_5.applymap(hot_encode)
    basket_5 = basket_encoded
    frq_items = apriori(basket_5, min_support=0.01, use_colnames=True)
    rules = association_rules(frq_items, metric="lift", min_threshold=1)
    rules = rules.sort_values(['confidence', 'lift'], ascending=[False, False])
    print(rules.head())
    print(frq_items.head())

    basket_8 = (df[df['sales_outlet_id'] == 8]
                .groupby(['transaction_id', 'product_id'])['quantity']
                .sum().unstack().reset_index().fillna(0)
                .set_index('transaction_id'))
    print(type(basket_8))
    print(basket_8.head(20))
    basket_encoded = basket_8.applymap(hot_encode)
    basket_8 = basket_encoded
    frq_items = apriori(basket_8, min_support=0.01, use_colnames=True)
    rules = association_rules(frq_items, metric="lift", min_threshold=1)
    rules = rules.sort_values(['confidence', 'lift'], ascending=[False, False])
    print(rules.head())
    print(frq_items.head())

    # Loading the Data
    #data = pd.read_csv('customer.csv')
    #print(data.head(7))


    # Exploring the columns of the data
    #print(data.columns)

    # Exploring the different regions of transactions
    # data.Country.unique()



    #df = pd.read_csv('data.csv', index_col=0)






    #########COMPARING YES/NO TRUE FALSE ###########
    #import pandas as pd
    #cereal_df = pd.read_csv("/tmp/tmp07wuam09/data/cereal.csv")
    #cereal_df2 = pd.read_csv("data/cereal.csv")

    # Are they the same?
    #print(pd.DataFrame.equals(cereal_df, cereal_df2))
