from collections import defaultdict
from .ballot import BallotSet
from fractions import Fraction


class Candidate:
    def __init__(self, name, votes):
        self.name = name
        self.votes = votes

    def __repr__(self):
        return "<Candidate {} with {} votes>".format(self.name, len(self.votes))

    def __str__(self):
        return self.name

    def __hash__(self):
        return hash(self.name)

    def transferable_votes(self, quota):
        transferable = defaultdict(BallotSet)
        if len(self.votes) <= quota:
            return transferable

        fraction = Fraction(len(self.votes) - quota, len(self.votes))

        for vote, count in self.votes:
            next_choice = vote.next_choice
            if next_choice is not None:
                transferable[next_choice].add(vote, count * fraction)

        return transferable
