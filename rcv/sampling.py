import random

from .schedule import PreferenceSchedule


class Sampler:
    def __init__(self, weighted_items):
        self.items = [item for item, weight in weighted_items]
        self.weights = [weight for item, weight in weighted_items]

    def __repr__(self):
        return "<Sampler items={} weights={}>".format(self.items, self.weights)

    def sample(self, k):
        return random.choices(self.items, weights=self.weights, k=k)


class PreferenceSampler(dict):
    """
    For sampling ballots from smaller units (e.g. precincts) with varying turnouts
    and aggregating them into a :class:`~rcv.PreferenceSchedule` for a larger area
    (e.g. the entire city, or a ward composed of multiple precincts).
    """

    def __init__(self, data):
        """
        :param data: a dictionary mapping each unit to the :class:`~rcv.BallotSet`
            to sample from.
        :type data: dict[any, BallotSet]
        """
        super().__init__({unit: Sampler(ballots) for unit, ballots in data.items()})

    def sample(self, turnouts):
        """
        Sample ballots from each unit to produce a :class:`~rcv.PreferenceSchedule`.
        The ``turnouts`` dictionary maps each unit to the total number of ballots
        to sample from that unit. If the user's goal is to sample from precincts
        to generate election results for a larger district, then these numbers
        would be each precinct's turnout for that election.

        :param turnouts: the turnouts for each unit
        :type turnouts: dict[any, Number]
        :returns: a :class:`~rcv.PreferenceSchedule` holding the sampled preferences
        :rtype: rcv.PreferenceSchedule
        """
        return PreferenceSchedule.from_ballots(
            ballot
            for unit, turnout in turnouts.items()
            for ballot in self[unit].sample(turnout)
        )
