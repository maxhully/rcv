import pytest
from rcv.candidate import Candidate
from rcv.ballot import BallotSet


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

        total_votes = candidate.total_votes
        surplus = total_votes - quota
        expected = {
            "Elizabeth": BallotSet(
                [(("Amy", "Elizabeth", "Kamala"), 10 * surplus / total_votes)]
            ),
            "Kamala": BallotSet([(("Amy", "Kamala"), 5 * surplus / total_votes)]),
        }

        assert set(expected.keys()) == set(transferable.keys())
        for key in expected:
            print(transferable[key], expected[key])
            assert transferable[key] == expected[key]

    def test_transferable_votes_is_empty_if_less_than_quota(self, candidate):
        quota = 1000
        transferable = candidate.transferable_votes(quota)
        
        assert len(transferable) == 0
        assert isinstance(transferable, dict)