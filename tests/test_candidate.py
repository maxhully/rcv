import pytest
from rcv.candidate import Candidate
from rcv.ballot import BallotSet
from fractions import Fraction


@pytest.fixture
def candidate():
    ballots = BallotSet([(("Amy", "Elizabeth", "Kamala"), 10), (("Amy", "Kamala"), 5)])
    amy = Candidate("Amy", ballots)
    return amy


class TestCandidate:
    def test_can_create(self, candidate):
        assert candidate

    def test_has_repr(self, candidate):
        assert repr(candidate) == "<Candidate Amy with 15 votes>"

    def test_str_is_name(self, candidate):
        assert str(candidate) == "Amy"

    def test_hash_by_name(self, candidate):
        assert hash(candidate) == hash("Amy")

    def test_transferable_votes(self, candidate):
        quota = 10
        transferable = candidate.transferable_votes(quota=quota)

        total_votes = len(candidate.votes)
        surplus = total_votes - quota
        expected = {
            "Elizabeth": BallotSet(
                [(("Amy", "Elizabeth", "Kamala"), 10 * Fraction(surplus / total_votes))]
            ),
            "Kamala": BallotSet(
                [(("Amy", "Kamala"), 5 * Fraction(surplus / total_votes))]
            ),
        }

        assert set(expected.keys()) == set(transferable.keys())
        for key in expected:
            assert transferable[key] == expected[key]
