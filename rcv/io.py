import pandas


def normalize_preferences(choices):
    new_choices = []
    for choice in choices:
        if choice and choice not in new_choices:
            new_choices.append(choice)
    return new_choices


def normalize_preference_schedule(schedule):
    records = [normalize_preferences(entries[1:]) for entries in schedule.itertuples()]

    normalized = pandas.DataFrame(
        data=records, columns=schedule.columns, index=schedule.index
    )
    return normalized
