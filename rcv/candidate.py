from .ballot import BallotSet


class Candidate:
    def __init__(self, name, votes=None):
        self.name = str(name)
        self.votes = BallotSet(votes)

    def __repr__(self):
        return "<Candidate {} with {} votes>".format(self.name, self.total_votes)

    def __str__(self):
        return self.name

    def __hash__(self):
        return hash(self.name)

    @property
    def total_votes(self):
        return self.votes.total_weight
