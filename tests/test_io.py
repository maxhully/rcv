from rcv.io import normalize_preferences


class TestNormalizePreferences:
    def test_removes_duplicates(self):
        prefs = ["A", "A", "B"]
        result = normalize_preferences(prefs)
        assert result == ["A", "B"]
