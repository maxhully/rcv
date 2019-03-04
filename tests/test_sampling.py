from rcv.sampling import PreferenceSampler, Sampler
from rcv.ballot import BallotSet

import pytest


@pytest.fixture
def data():
    d = {
        "Precinct 1": {
            ("black", "nan", "nan"): 17.887,
            ("hispanic", "white", "white"): 2.005,
            ("white", "white", "asian"): 12.168,
            ("white", "asian", "white"): 11.098,
            ("white", "nan", "nan"): 164.294,
        },
        "Precinct 2": {
            ("asian", "white", "black"): 1.966,
            ("black", "hispanic", "nan"): 0.402,
            ("white", "white", "white"): 233.795,
            ("hispanic", "black", "white"): 2.560,
            ("hispanic", "nan", "nan"): 2.502,
        },
    }
    return {key: BallotSet(distribution.items()) for key, distribution in d.items()}


@pytest.fixture
def sampler(data):
    return PreferenceSampler(data)


class TestSampler:
    def test_can_create_from_ballot_set(self, ballots):
        sampler = Sampler(ballots)
        assert sampler

    def test_repr(self):
        sampler = Sampler([("a", 10), ("b", 5)])
        assert repr(sampler) == "<Sampler items=['a', 'b'] weights=[10, 5]>"


class TestPreferenceSampler:
    def test_create_from_data_dictionary(self, data):
        sampler = PreferenceSampler(data)
        assert sampler

    def test_can_sample_with_turnouts(self, sampler):
        schedule = sampler.sample(turnouts={"Precinct 1": 10, "Precinct 2": 15})
        assert schedule.total_votes == 25
