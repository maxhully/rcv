import pandas


def normalize_preferences(choices):
    new_choices = []
    for choice in choices:
        if choice != 0 and choice not in new_choices:
            new_choices.append(choice)
    return new_choices


def normalize_preference_schedules(schedules):
    records = [normalize_preferences(entries[1:]) for entries in schedules.itertuples()]

    normalized = pandas.DataFrame(
        data=records, columns=schedules.columns, index=schedules.index
    )
    return normalized
