from rcv.ballot import BallotSet


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
        expected = BallotSet(
            [
                (("Elizabeth", "Kamala"), 10 * surplus / total_votes),
                (("Kamala",), 5 * surplus / total_votes),
            ]
        )

        assert transferable == expected

    def test_transferable_votes_is_empty_if_less_than_quota(self, candidate):
        quota = 1000
        transferable = candidate.transferable_votes(quota)

        assert transferable.is_empty
