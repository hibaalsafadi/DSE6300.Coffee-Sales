from mlxtend.frequent_patterns import apriori, association_rules


def hot_encode(x):
    if x <= 0:
        return 0
    if x >= 1:
        return 1


def SR(df, kafka_producer):
    df.show()
    df = df.toPandas()
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
    kafka_producer.send('results', frq_items.to_json())
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
    kafka_producer.send('results', frq_items.to_json())
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
    kafka_producer.send('results', frq_items.to_json())

