from rcv.candidate import Candidate
from rcv.schedule import PreferenceSchedule
from rcv.stv import FractionalSTV, droop_quota, find_winners


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
        stv = FractionalSTV(ballots, quota=droop_quota)
        winners = stv.elect(seats=2)
        assert list(winners) == ["Amy", "Kamala"]

    def test_can_find_candidates_from_ballots(self, ballots):
        stv = FractionalSTV(ballots)
        assert len(stv.candidates) == 3
        assert set(candidate.name for candidate in stv.candidates) == {
            "Amy",
            "Elizabeth",
            "Kamala",
        }

    def test_declare_winner(self, ballots):
        amy = Candidate("Amy")
        kamala = Candidate("Kamala")
        elizabeth = Candidate("Elizabeth")
        schedule = PreferenceSchedule(ballots, candidates={amy, kamala, elizabeth})
        stv = FractionalSTV(schedule)

        stv.declare_winner(amy, 21)

        assert amy.votes.is_empty
        assert amy in stv.elected
        assert amy not in stv.candidates

        assert kamala.total_votes > 20
