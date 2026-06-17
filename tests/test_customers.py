def test_remove_null_customer_id(spark):

    data = [
        ("e1", "c1"),
        ("e2", None)
    ]

    df = spark.createDataFrame(
        data,
        ["event_id", "customer_id"]
    )

    result = clean_events(df)

    assert result.count() == 1