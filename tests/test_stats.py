import unittest
from basketball_toolkit import summarize_player, summarize_games

class StatsTests(unittest.TestCase):
    def test_weighted_percentages(self):
        data = [
            {"points": 10, "fgm": 1, "fga": 2, "tpm": 0, "tpa": 0},
            {"points": 20, "fgm": 3, "fga": 8, "tpm": 1, "tpa": 2},
        ]
        s = summarize_player(data)
        self.assertEqual(s["games"], 2)
        self.assertEqual(s["fg_pct"], 40.0)
        self.assertEqual(s["per_game"]["points"], 15.0)
    def test_empty(self):
        self.assertIsNone(summarize_player([])["fg_pct"])
    def test_invalid(self):
        with self.assertRaises(ValueError):
            summarize_player([{"fgm": 3, "fga": 2}])
        with self.assertRaises(ValueError):
            summarize_player([{"points": "-1"}])
    def test_grouping(self):
        s = summarize_games([{"player_id": "P01", "points": 8}, {"player_id": "P02", "points": 12}])
        self.assertEqual(s["P01"]["totals"]["points"], 8)

if __name__ == "__main__":
    unittest.main()
