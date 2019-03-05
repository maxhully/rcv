from rcv.sampling import PreferenceSampler
from rcv.ballot import BallotSet
from rcv.schedule import PreferenceSchedule

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


class TestPreferenceSampler:
    def test_create_from_data_dictionary(self, data):
        sampler = PreferenceSampler(data)
        assert sampler

    def test_can_sample_with_turnouts(self, sampler):
        schedule = sampler.sample(turnouts={"Precinct 1": 10, "Precinct 2": 15})
        assert schedule.total_votes == 25
        assert isinstance(schedule, PreferenceSchedule)

    def test_repr(self, sampler):
        assert repr(sampler) == "<PreferenceSampler units=[Precinct 1, Precinct 2]>"

    def test_repr_with_int_keys(self):
        sampler = PreferenceSampler({1: BallotSet()})
        assert repr(sampler) == "<PreferenceSampler units=[1]>"
