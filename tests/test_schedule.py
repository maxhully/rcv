from rcv import PreferenceSchedule
from rcv.schedule import WeightedBallot


class TestPreferenceSchedule:
    def test_create_from_dataframe(self, dataframe):
        schedule = PreferenceSchedule.from_dataframe(dataframe)
        assert schedule

    def test_preferences_are_weighted_ballots(self, schedule):
        assert all(isinstance(ballot, WeightedBallot) for ballot in schedule)

    def test_gives_expected_counts(self, schedule):
        assert set(schedule) == {
            WeightedBallot(("Amy", "Elizabeth", "Kamala"), 2),
            WeightedBallot(("Elizabeth", "Kamala", "Amy"), 4),
            WeightedBallot(("Kamala", "Elizabeth", "Amy"), 2),
        }


class TestWeightedBallot:
    def test_implements_repr(self, ballot):
        assert repr(ballot) == "<WeightedBallot (Kamala, Elizabeth, Amy) weight=2>"

    def test_can_eliminate_candidate(self, ballot):
        ballot.eliminate("Kamala")
        return ballot == WeightedBallot(("Elizabeth", "Amy"), 2)

    def test_can_change_weight_with_multiplication(self, ballot):
        ballot *= 4
        assert ballot == WeightedBallot(("Kamala", "Elizabeth", "Amy"), 8)

    def test_has_top_choice_property(self, ballot):
        assert ballot.top_choice == "Kamala"

    def test_has_is_empty_property(self, ballot):
        assert ballot.is_empty is False
        assert WeightedBallot([], 1).is_empty is True
