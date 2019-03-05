from .schedule import PreferenceSchedule
from .ballot import BallotSet


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
        super().__init__(
            {
                unit: BallotSet(ballots, weight_type=float)
                for unit, ballots in data.items()
            }
        )

    def __repr__(self):
        units = "[" + ", ".join(str(key) for key in self.keys()) + "]"
        return "<PreferenceSampler units={}>".format(units)

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
        ballots = BallotSet(weight_type=float)
        for unit, turnout in turnouts.items():
            ballots.update(self[unit] * turnout)
        total_turnout = sum(turnouts.values())
        return PreferenceSchedule.from_ballots(ballots.sample(total_turnout))
