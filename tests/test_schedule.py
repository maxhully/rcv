from rcv import PreferenceSchedule
from rcv.schedule import Ballot
from numbers import Number


class TestPreferenceSchedule:
    def test_create_from_dataframe(self, dataframe):
        schedule = PreferenceSchedule.from_dataframe(dataframe)
        assert schedule

    def test_preferences_are_weighted_ballots(self, schedule):
        assert all(
            isinstance(ballot, Ballot) and isinstance(weight, Number)
            for ballot, weight in schedule
        )

    def test_gives_expected_counts(self, schedule):
        assert set(schedule) == {
            (Ballot(("Amy", "Elizabeth", "Kamala")), 2),
            (Ballot(("Elizabeth", "Kamala", "Amy")), 4),
            (Ballot(("Kamala", "Elizabeth", "Amy")), 2),
        }
