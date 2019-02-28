from collections import defaultdict
from .ballot import BallotSet


class Candidate:
    def __init__(self, name, votes):
        self.name = name
        self.votes = votes

    def __repr__(self):
        return "<Candidate {} with {} votes>".format(self.name, self.total_votes)

    def __str__(self):
        return self.name

    def __hash__(self):
        return hash(self.name)

    @property
    def total_votes(self):
        return self.votes.total_weight

    def transferable_votes(self, quota):
        transferable = defaultdict(BallotSet)
        total = self.total_votes
        if total <= quota:
            return transferable

        fraction = (total - quota) / total

        for vote, count in self.votes:
            next_choice = vote.next_choice
            if next_choice is not None:
                transferable[next_choice].add(vote, count * fraction)

        return transferable
