from transformations.products import normalize_products


def test_remove_invalid_price(spark):

    data = [
        ("p1", 100),
        ("p2", -50),
        ("p3", 0)
    ]

    df = spark.createDataFrame(
        data,
        ["product_id", "price"]
    )

    result = normalize_products(df)

    assert result.count() == 1