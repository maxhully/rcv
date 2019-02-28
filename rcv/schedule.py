from .ballot import Ballot
from .weighted_set import WeightedSet


class PreferenceSchedule:
    """A reduced preference schedule"""

    def __init__(self, ballots, candidates):
        self.ballots = ballots
        self.candidates = candidates

    def __iter__(self):
        return iter(self.ballots)

    @classmethod
    def from_dataframe(cls, df):
        """Create a preference schedule from a dataframe whose rows are ballots.
        That is, the first column is the first-ranked candidate for each ballot,
        the second is the second-ranked candidate, and so on."""
        grouped_ballots = df.groupby(list(df.columns)).size().items()

        ballots = WeightedSet(
            (Ballot(ranking), count) for ranking, count in grouped_ballots
        )

        candidates = set(df.values.ravel())
        return cls(ballots, candidates)
