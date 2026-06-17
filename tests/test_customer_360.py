
# from gold.build_customer_360 import build_customer_360

# def test_total_spent_per_customer(spark):

#     data = [
#         ("c1", "purchase", 100),
#         ("c1", "purchase", 200),
#         ("c2", "purchase", 50)
#     ]

#     df = spark.createDataFrame(
#         data,
#         ["customer_id", "event_type", "price"]
#     )

#     result = build_customer_360(df)

#     c1 = result.filter(
#         result.customer_id == "c1"
#     ).collect()[0]

#     assert c1.total_spent == 300