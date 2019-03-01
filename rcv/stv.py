import math

from .schedule import PreferenceSchedule


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
    def __init__(self, schedule, quota=droop_quota):
        if not isinstance(schedule, PreferenceSchedule):
            schedule = PreferenceSchedule(schedule)
        self.quota_func = quota
        self.schedule = schedule
        self.total_votes = schedule.total_votes
        self.elected = set()

    @property
    def candidates(self):
        return self.schedule.candidates

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
                self.schedule.eliminate(least)

    def declare_winner(self, winner, quota):
        self.schedule.distribute_ballots(winner.transferable_votes(quota))
        self.elected.add(winner)
        self.schedule.remove_candidate(winner)
