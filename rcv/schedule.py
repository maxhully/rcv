class WeightedBallot:
    def __init__(self, preferences, weight):
        self.preferences = list(preferences)
        self.weight = weight

    def __repr__(self):
        names = "({})".format(", ".join(map(str, self.preferences)))
        return "<WeightedBallot {} weight={}>".format(names, self.weight)

    def __len__(self):
        return len(self.preferences)

    def __iter__(self):
        return iter(self.preferences)

    def eliminate(self, candidate):
        self.preferences.remove(candidate)

    @property
    def top_choice(self):
        return self.preferences[0]

    @property
    def is_empty(self):
        return len(self) == 0

    def __imul__(self, multiplier):
        self.weight *= multiplier
        return self

    def __eq__(self, ballot):
        return (
            len(ballot) == len(self)
            and all(left == right for left, right in zip(self, ballot))
            and ballot.weight == self.weight
        )

    def __hash__(self):
        return hash(self.weight) + hash(tuple(self))


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

        ballots = [WeightedBallot(ranking, count) for ranking, count in grouped_ballots]

        candidates = set(df.values.ravel())
        return cls(ballots, candidates)
