import math

from .schedule import PreferenceSchedule
from .ballot import BallotSet


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
    def __init__(self, schedule, seats, quota=droop_quota):
        if not isinstance(schedule, PreferenceSchedule):
            schedule = PreferenceSchedule(schedule)
        self.seats = seats
        self.schedule = schedule
        if callable(quota):
            self.quota = quota(schedule.total_votes, seats)
        else:
            self.quota = quota
        self.elected = set()

    @property
    def candidates(self):
        return self.schedule.candidates

    def elect(self):
        while len(self.elected) < self.seats:
            winners = find_winners(self.candidates, self.quota)
            if len(winners) > 0:
                for winner in winners:
                    yield str(winner)
                    self.declare_winner(winner)
            else:
                least = find_least(self.candidates)
                self.schedule.eliminate(least)

    def declare_winner(self, winner):
        ballots_to_transfer = self.transferable_votes(winner)
        self.schedule.distribute_ballots(ballots_to_transfer)
        self.elected.add(winner)
        self.schedule.remove_candidate(winner)

    def transferable_votes(self, candidate):
        total = candidate.total_votes
        quota = self.quota

        if total <= quota:
            return BallotSet()

        fraction = (total - quota) / total
        transferable = BallotSet()
        for vote, count in candidate.votes:
            next_choice = vote.next_choice
            if next_choice is not None:
                transferable.add(vote.eliminate(candidate), count * fraction)

        return transferable
