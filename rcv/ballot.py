from .weighted_set import WeightedSet


class Ballot(tuple):
    def __repr__(self):
        names = "({})".format(", ".join(map(str, self)))
        return "<Ballot {}>".format(names)

    def eliminate(self, eliminated_candidate):
        return self.__class__(
            candidate for candidate in self if candidate != eliminated_candidate
        )

    @property
    def top_choice(self):
        return self[0]

    @property
    def is_empty(self):
        return len(self) == 0


class BallotSet(WeightedSet):
    def __init__(self, weighted_items):
        super().__init__((Ballot(item), weight) for item, weight in weighted_items)

    def eliminate(self, eliminated_candidate):
        return self.__class__(
            (ballot.eliminate(eliminated_candidate), weight)
            for (ballot, weight) in self
        )
