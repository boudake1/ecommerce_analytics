from transformations.events import clean_events


def test_remove_duplicate_events(spark):

    data = [
        ("e1", "c1"),
        ("e1", "c1"),
        ("e2", "c2")
    ]

    df = spark.createDataFrame(
        data,
        ["event_id", "customer_id"]
    )

    result = clean_events(df)

    assert result.count() == 2