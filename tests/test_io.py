from pandas import DataFrame

from rcv.io import normalize_preference_schedule, normalize_preferences


class TestNormalizePreferences:
    def test_removes_duplicates(self):
        prefs = ["A", "A", "B"]
        result = normalize_preferences(prefs)
        assert result == ["A", "B"]

    def test_skips_falsy_values(self):
        assert normalize_preferences([None, None, "Amy", 0]) == ["Amy"]

    def test_can_normalize_a_dataframe(self):
        df = DataFrame(
            {
                "first": [None, "Amy", "Amy", "Kamala"],
                "second": ["Elizabeth", "Elizabeth", "Amy", "Amy"],
                "third": ["Kamala", "Kamala", "Elizabeth", "Elizabeth"],
            }
        )
        expected = DataFrame(
            {
                "first": ["Elizabeth", "Amy", "Amy", "Kamala"],
                "second": ["Kamala", "Elizabeth", "Elizabeth", "Amy"],
                "third": [None, "Kamala", None, "Elizabeth"],
            }
        )
        result = normalize_preference_schedule(df)
        assert result.equals(expected)
