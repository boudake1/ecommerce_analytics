def clean_events(df):

    return (
        df
        .dropDuplicates(["event_id"])
    )