# def test_product_views(spark):

#     data = [
#         ("p1", "product_view"),
#         ("p1", "product_view"),
#         ("p1", "purchase")
#     ]

#     df = spark.createDataFrame(
#         data,
#         ["product_id", "event_type"]
#     )

#     result = build_product_performance(df)

#     row = result.collect()[0]

#     assert row.views == 2