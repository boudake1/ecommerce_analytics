# transformations/cleaning.py
from pyspark.sql import functions as F

def clean_events(df):

    return (
        df
        .dropDuplicates(["event_id"])
        .filter("user_id IS NOT NULL")
        .filter("event_type IN ('product_view', 'purchase', 'add_to_cart', 'remove_from_cart', 'search')")
        .filter("price > 0")
    )

