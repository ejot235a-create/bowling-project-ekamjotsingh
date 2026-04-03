"""
Bowling Game Implementation
A module for calculating ten-pin bowling game scores.

This module implements the scoring logic for a ten-pin bowling game,
following official scoring rules including strikes, spares, and the
special 10th frame rules. The implementation validates all inputs and
game state to ensure consistent, correct scoring.

Classes:
    BowlingGame: Main class for managing a single game session
    
Example Usage:
    game = BowlingGame()
    game.roll(10)  # Strike
    game.roll(3)
    game.roll(6)
    for _ in range(16):
        game.roll(0)
    print(game.score())  # Output: 28
"""


class BowlingGame:
    """
    Represents a single ten-pin bowling game.

    This class manages a single player's bowling game according to
    official ten-pin bowling rules. Rolls are recorded sequentially
    and validated for consistency with bowling rules. The final score
    is calculated according to standard scoring with strike and spare
    bonuses.

    Attributes:
        rolls (list[int]): List of all rolls in the game, in order.
                          Each element represents pins knocked down.

    Raises:
        TypeError: If non-integer values are provided for pins.
        ValueError: If pins are out of valid range or game state is invalid.
    """

    def __init__(self) -> None:
        """
        Initialize a new bowling game with no rolls recorded.

        Sets up an empty rolls list and initializes the game instance
        ready to accept roll inputs.
        """
        self.rolls: list[int] = []

    def roll(self, pins: object) -> None:
        """
        Record a roll in the current game.

        Validates that the input is an integer in the range 0-10, then
        records the roll and validates the current game state for consistency.
        Each call to roll() represents one ball thrown by the player.

        Args:
            pins (int): Number of pins knocked down on this roll. Must be
                       an integer in range [0, 10]. Boolean values are
                       explicitly rejected even though bool is subclass of int.

        Raises:
            TypeError: If pins is not an integer type or if pins is a boolean.
            ValueError: If pins is outside valid range [0, 10].
            ValueError: If adding this roll creates an invalid game state
                       (e.g., frame total exceeds 10 in frames 1-9).

        Note:
            - Frame totals cannot exceed 10 except in the 10th frame
            - The 10th frame allows up to 3 rolls if strike/spare is achieved
            - Game state validation happens immediately after adding roll
        """
        if isinstance(pins, bool) or not isinstance(pins, int):
            raise TypeError("pins must be an integer")

        if pins < 0 or pins > 10:
            raise ValueError("pins must be between 0 and 10")

        self.rolls.append(pins)
        self._validate_game_state()

    def score(self) -> int:
        """
        Calculate the total score for the game.

        Returns:
            int: Total bowling score.

        Raises:
            ValueError: If the game is incomplete or invalid.
        """
        self._validate_game_complete()

        score: int = 0
        frame_index: int = 0

        for _ in range(10):
            if self._is_strike(frame_index):
                score += 10 + self._strike_bonus(frame_index)
                frame_index += 1
            elif self._is_spare(frame_index):
                score += 10 + self._spare_bonus(frame_index)
                frame_index += 2
            else:
                score += self._sum_of_balls_in_frame(frame_index)
                frame_index += 2

        return score

    def _is_strike(self, frame_index: int) -> bool:
        """Return True if the roll at frame_index is a strike."""
        return self.rolls[frame_index] == 10

    def _is_spare(self, frame_index: int) -> bool:
        """Return True if the two rolls at frame_index make a spare."""
        return self.rolls[frame_index] + self.rolls[frame_index + 1] == 10

    def _strike_bonus(self, frame_index: int) -> int:
        """Return strike bonus from the next two rolls."""
        return self.rolls[frame_index + 1] + self.rolls[frame_index + 2]

    def _spare_bonus(self, frame_index: int) -> int:
        """Return spare bonus from the next roll."""
        return self.rolls[frame_index + 2]

    def _sum_of_balls_in_frame(self, frame_index: int) -> int:
        """Return the total for an open frame."""
        return self.rolls[frame_index] + self.rolls[frame_index + 1]

    def _validate_game_complete(self) -> None:
        """
        Validate that the game has enough rolls to calculate a score.

        Raises:
            ValueError: If the game is incomplete or invalid.
        """
        frame_index = 0

        for frame in range(10):
            if frame_index >= len(self.rolls):
                raise ValueError("game is incomplete")

            if self._is_strike(frame_index):
                frame_index += 1
                if frame == 9:
                    if len(self.rolls) < frame_index + 2:
                        raise ValueError("game is incomplete")
            else:
                if frame_index + 1 >= len(self.rolls):
                    raise ValueError("game is incomplete")

                if self.rolls[frame_index] + self.rolls[frame_index + 1] > 10:
                    raise ValueError("invalid frame score")

                if self._is_spare(frame_index):
                    frame_index += 2
                    if frame == 9 and len(self.rolls) < frame_index + 1:
                        raise ValueError("game is incomplete")
                else:
                    frame_index += 2

        if len(self.rolls) > frame_index + 2:
            raise ValueError("too many rolls in game")

    def _validate_game_state(self) -> None:
        """
        Validate the current rolls entered so far.

        Raises:
            ValueError: If the roll sequence is invalid.
        """
        frame_index = 0
        frame = 0

        while frame < 9 and frame_index < len(self.rolls):
            first = self.rolls[frame_index]

            if first == 10:
                frame_index += 1
            else:
                if frame_index + 1 < len(self.rolls):
                    second = self.rolls[frame_index + 1]
                    if first + second > 10:
                        raise ValueError("invalid frame score")
                frame_index += 2

            frame += 1