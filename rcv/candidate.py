from .ballot import BallotSet


class Candidate:
    def __init__(self, name, votes=None):
        self.name = name
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

    def transferable_votes(self, quota):
        transferable = BallotSet()
        total = self.total_votes
        if total <= quota:
            return transferable

        surplus = total - quota

        fraction = surplus / total

        for vote, count in self.votes:
            next_choice = vote.next_choice
            if next_choice is not None:
                transferable.add(vote.eliminate(self), count * fraction)

        return transferable
