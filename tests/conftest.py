import pandas
import pytest

from rcv import PreferenceSchedule
from rcv.schedule import WeightedBallot


@pytest.fixture
def dataframe():
    return pandas.DataFrame(
        [
            ("Amy", "Elizabeth", "Kamala"),
            ("Amy", "Elizabeth", "Kamala"),
            ("Elizabeth", "Kamala", "Amy"),
            ("Elizabeth", "Kamala", "Amy"),
            ("Elizabeth", "Kamala", "Amy"),
            ("Elizabeth", "Kamala", "Amy"),
            ("Kamala", "Elizabeth", "Amy"),
            ("Kamala", "Elizabeth", "Amy"),
        ]
    )


@pytest.fixture
def schedule(dataframe):
    return PreferenceSchedule.from_dataframe(dataframe)


@pytest.fixture
def ballot():
    return WeightedBallot(("Kamala", "Elizabeth", "Amy"), 2)
