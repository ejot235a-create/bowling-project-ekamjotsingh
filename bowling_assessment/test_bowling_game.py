import unittest
from bowling_game import BowlingGame


class TestBowlingGame(unittest.TestCase):
    def setUp(self):
        self.game = BowlingGame()

    def roll_many(self, n: int, pins: int) -> None:
        for _ in range(n):
            self.game.roll(pins)

    def roll_spare(self):
        self.game.roll(5)
        self.game.roll(5)

    def roll_strike(self):
        self.game.roll(10)

    def test_gutter_game_scores_zero(self):
        self.roll_many(20, 0)
        self.assertEqual(self.game.score(), 0)

    def test_all_ones_scores_twenty(self):
        self.roll_many(20, 1)
        self.assertEqual(self.game.score(), 20)

    def test_one_spare_scores_correctly(self):
        self.roll_spare()
        self.game.roll(3)
        self.roll_many(17, 0)
        self.assertEqual(self.game.score(), 16)

    def test_one_strike_scores_correctly(self):
        self.roll_strike()
        self.game.roll(3)
        self.game.roll(4)
        self.roll_many(16, 0)
        self.assertEqual(self.game.score(), 24)

    def test_perfect_game_scores_three_hundred(self):
        self.roll_many(12, 10)
        self.assertEqual(self.game.score(), 300)

    def test_open_frame_is_counted_correctly(self):
        self.game.roll(3)
        self.game.roll(6)
        self.roll_many(18, 0)
        self.assertEqual(self.game.score(), 9)

    def test_tenth_frame_spare(self):
        self.roll_many(18, 0)
        self.game.roll(5)
        self.game.roll(5)
        self.game.roll(7)
        self.assertEqual(self.game.score(), 17)

    def test_tenth_frame_strike(self):
        self.roll_many(18, 0)
        self.game.roll(10)
        self.game.roll(7)
        self.game.roll(2)
        self.assertEqual(self.game.score(), 19)

    def test_consecutive_strikes(self):
        self.game.roll(10)
        self.game.roll(10)
        self.game.roll(4)
        self.game.roll(2)
        self.roll_many(14, 0)
        self.assertEqual(self.game.score(), 46)

    def test_invalid_negative_roll_raises_error(self):
        with self.assertRaises(ValueError):
            self.game.roll(-1)

    def test_invalid_roll_over_ten_raises_error(self):
        with self.assertRaises(ValueError):
            self.game.roll(11)

    def test_non_integer_roll_raises_error(self):
        with self.assertRaises(TypeError):
            self.game.roll("5")

    def test_boolean_roll_raises_error(self):
        with self.assertRaises(TypeError):
            self.game.roll(True)

    def test_invalid_frame_total_raises_error(self):
        self.game.roll(8)
        with self.assertRaises(ValueError):
            self.game.roll(5)

    def test_incomplete_game_raises_error(self):
        self.game.roll(10)
        with self.assertRaises(ValueError):
            self.game.score()


if __name__ == "__main__":
    unittest.main()