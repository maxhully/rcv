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
        return hash((tuple(self), self.weight))
