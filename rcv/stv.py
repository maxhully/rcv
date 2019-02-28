import math

from .ballot import BallotSet
from .candidate import Candidate


def find_winners(candidates, quota):
    print(candidates, quota)
    return {candidate for candidate in candidates if candidate.total_votes >= quota}


def find_least(candidates):
    iter_candidates = iter(candidates)
    least = next(iter_candidates)
    for candidate in candidates:
        if candidate.total_votes < least.total_votes:
            least = candidate
    return least


def droop_quota(number_of_votes, number_of_seats):
    return math.floor(number_of_votes / (number_of_seats + 1)) + 1


class FractionalSTV:
    def __init__(self, ballots, candidates=None, quota=droop_quota):
        self.quota_func = quota

        if candidates is None:
            names = {name for ballot, weight in ballots for name in ballot}
            candidates = {Candidate(name) for name in names}

        self.candidates = set(candidates)
        self._candidates_by_name = {
            str(candidate): candidate for candidate in self.candidates
        }

        self.distribute_ballots(ballots)
        self.total_votes = sum(candidate.total_votes for candidate in self.candidates)
        self.elected = set()

    def elect(self, seats):
        quota = self.quota_func(self.total_votes, seats)
        while len(self.elected) < seats:
            winners = find_winners(self.candidates, quota)
            if len(winners) > 0:
                for winner in winners:
                    yield str(winner)
                    self.declare_winner(winner, quota)
            else:
                least = find_least(self.candidates)
                self.eliminate(least)

    def declare_winner(self, winner, quota):
        self.distribute_ballots(winner.transferable_votes(quota))
        winner.votes = BallotSet()
        self.elected.add(winner)
        self.remove_candidate(winner)

    def remove_candidate(self, removed):
        for candidate in self.candidates:
            if candidate is not removed:
                candidate.votes = candidate.votes.eliminate(removed)
        self.candidates.remove(removed)
        del self._candidates_by_name[str(removed)]

    def distribute_ballots(self, ballots):
        for ballot, weight in ballots:
            if not ballot.is_empty:
                candidate = self._candidates_by_name[ballot.top_choice]
                candidate.votes.add(ballot, weight)

    def eliminate(self, eliminated):
        self.distribute_ballots(eliminated.votes.eliminate(eliminated))
        self.remove_candidate(eliminated)
