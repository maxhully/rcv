import pandas
import pytest

from rcv import PreferenceSchedule
from rcv.ballot import Ballot, BallotSet


@pytest.fixture
def items():
    return [
        ("Amy", "Elizabeth", "Kamala"),
        ("Amy", "Elizabeth", "Kamala"),
        ("Elizabeth", "Kamala", "Amy"),
        ("Elizabeth", "Kamala", "Amy"),
        ("Elizabeth", "Kamala", "Amy"),
        ("Elizabeth", "Kamala", "Amy"),
        ("Kamala", "Elizabeth", "Amy"),
        ("Kamala", "Elizabeth", "Amy"),
    ]


@pytest.fixture
def dataframe(items):
    return pandas.DataFrame(items)


@pytest.fixture
def schedule(dataframe):
    return PreferenceSchedule.from_dataframe(dataframe)


@pytest.fixture
def ballot():
    return Ballot(("Kamala", "Elizabeth", "Amy"))


@pytest.fixture
def ballot_set(items):
    return BallotSet.from_items(items)
