import pandas
import pytest

from rcv import PreferenceSchedule
from rcv.ballot import Ballot, BallotSet
from rcv.candidate import Candidate


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


@pytest.fixture
def candidate():
    ballots = BallotSet([(("Amy", "Elizabeth", "Kamala"), 10), (("Amy", "Kamala"), 5)])
    amy = Candidate("Amy", ballots)
    return amy


@pytest.fixture
def candidates():
    amy = Candidate(
        "Amy", [(("Amy", "Elizabeth", "Kamala"), 20), (("Amy", "Kamala"), 5)]
    )
    kamala = Candidate(
        "Kamala", [(("Kamala",), 10), (("Kamala", "Elizabeth", "Amy"), 10)]
    )
    elizabeth = Candidate(
        "Elizabeth", [(("Elizabeth", "Amy"), 12), (("Elizabeth", "Kamala", "Amy"), 4)]
    )
    return {amy, kamala, elizabeth}
