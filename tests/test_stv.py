import pytest

from rcv.schedule import PreferenceSchedule
from rcv.stv import FractionalSTV, droop_quota, find_winners
from rcv.ballot import BallotSet
from fractions import Fraction


@pytest.fixture
def stv(ballots):
    schedule = PreferenceSchedule(ballots)
    return FractionalSTV(schedule, seats=2)


def test_find_winners(candidates):
    winners = find_winners(candidates, 20)
    assert {winner.name for winner in winners} == {"Kamala", "Amy"}

    winners = find_winners(candidates, 21)
    assert {winner.name for winner in winners} == {"Amy"}


def test_droop_quota():
    quota = droop_quota(number_of_votes=61, number_of_seats=2)
    assert quota == 21


class TestFractionalSTV:
    def test_elect(self, ballots):
        stv = FractionalSTV(ballots, seats=2, quota=droop_quota)
        winners = stv.elect()
        assert list(winners) == ["Amy", "Kamala"]

    def test_can_find_candidates_from_ballots(self, stv):
        assert len(stv.candidates) == 3
        assert set(candidate.name for candidate in stv.candidates) == {
            "Amy",
            "Elizabeth",
            "Kamala",
        }

    def test_declare_winner(self, stv):
        amy = stv.candidates["Amy"]
        kamala = stv.candidates["Kamala"]

        stv.declare_winner(amy)

        assert amy.votes.is_empty
        assert amy in stv.elected
        assert amy not in stv.candidates

        assert kamala.total_votes > 20

    def test_transferable_votes(self, stv):
        quota = stv.quota
        candidate = stv.candidates["Amy"]
        transferable = stv.transferable_votes(candidate)

        total_votes = candidate.total_votes
        surplus = total_votes - quota
        expected = BallotSet(
            [
                (("Elizabeth", "Kamala"), Fraction(20 * surplus, total_votes)),
                (("Kamala",), Fraction(5 * surplus, total_votes)),
            ]
        )

        print(expected)
        print(transferable)

        assert transferable == expected

    def test_transferable_votes_is_empty_if_less_than_quota(self, ballots):
        quota = 1000
        stv = FractionalSTV(ballots, seats=2, quota=quota)
        transferable = stv.transferable_votes(stv.candidates["Amy"])

        assert transferable.is_empty

    def test_can_pass_in_numerical_quota(self, ballots):
        stv = FractionalSTV(ballots, seats=2, quota=15)
        assert stv.quota == 15

    def test_can_handle_multiple_winners_in_first_round(self, ballots):
        stv = FractionalSTV(ballots, seats=3)
        assert set(stv.elect()) == {"Amy", "Elizabeth", "Kamala"}

    def test_against_real_data(self):
        ballots = BallotSet(
            [
                ((87, 402, 396), 1),
                ((393,), 10),
                ((393, 394, 397), 1),
                ((393, 394, 402), 1),
                ((393, 397), 1),
                ((393, 397, 399), 2),
                ((393, 397, 402), 5),
                ((393, 399), 2),
                ((393, 399, 395), 1),
                ((393, 399, 396), 1),
                ((393, 399, 397), 4),
                ((393, 399, 400), 3),
                ((393, 399, 402), 1),
                ((393, 402, 395), 2),
                ((393, 402, 397), 3),
                ((393, 402, 399), 1),
                ((394, 395), 1),
                ((396, 397, 402), 1),
                ((397,), 1),
                ((397, 393), 1),
                ((397, 393, 399), 1),
                ((397, 393, 400), 1),
                ((397, 398, 394), 1),
                ((397, 399, 395), 1),
                ((397, 399, 402), 4),
                ((397, 402, 393), 3),
                ((397, 402, 399), 1),
                ((397, 402, 401), 1),
                ((398,), 2),
                ((398, 394, 393), 1),
                ((398, 395, 396), 1),
                ((398, 399), 2),
                ((399, 393, 397), 1),
                ((399, 394, 400), 1),
                ((399, 395, 393), 1),
                ((399, 395, 397), 3),
                ((399, 395, 402), 2),
                ((399, 397, 395), 1),
                ((399, 397, 402), 4),
                ((399, 400, 396), 1),
                ((399, 401, 398), 1),
                ((399, 402, 393), 3),
                ((399, 402, 397), 3),
                ((400, 393, 397), 1),
                ((400, 394, 393), 1),
                ((402,), 1),
                ((402, 393), 1),
                ((402, 393, 397), 1),
                ((402, 393, 399), 4),
                ((402, 395, 399), 1),
                ((402, 397, 87), 1),
                ((402, 397, 399), 1),
                ((402, 397, 401), 1),
                ((402, 399, 393), 1),
                ((402, 399, 395), 2),
                ((402, 399, 397), 2),
            ]
        )
        stv = FractionalSTV(ballots, seats=4)

        assert list(stv.elect()) == ["393", "399", "397", "402"]
