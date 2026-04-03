"""
Bowling Game Implementation
A module for calculating ten-pin bowling game scores.
"""


class BowlingGame:
    MAX_PINS = 10
    TOTAL_FRAMES = 10

    def __init__(self) -> None:
        self.rolls: list[int] = []

    def roll(self, pins: object) -> None:
        if isinstance(pins, bool) or not isinstance(pins, int):
            raise TypeError("Pins must be an integer")

        if pins < 0 or pins > self.MAX_PINS:
            raise ValueError("Pins must be between 0 and 10")

        # 🚨 Prevent extra rolls after game is complete
        if self._is_game_complete():
            raise ValueError("Cannot roll after game is complete")

        self.rolls.append(pins)
        self._validate_game_state()

    def score(self) -> int:
        self._validate_game_complete()

        score = 0
        frame_index = 0

        for _ in range(self.TOTAL_FRAMES):

            if self._is_strike(frame_index):
                score += self.MAX_PINS + self._strike_bonus(frame_index)
                frame_index += 1

            elif self._is_spare(frame_index):
                score += self.MAX_PINS + self._spare_bonus(frame_index)
                frame_index += 2

            else:
                score += self._sum_of_balls_in_frame(frame_index)
                frame_index += 2

        return score

    def _is_game_complete(self) -> bool:
        try:
            self._validate_game_complete()
            return True
        except ValueError:
            return False

    def _is_strike(self, index: int) -> bool:
        return self.rolls[index] == self.MAX_PINS

    def _is_spare(self, index: int) -> bool:
        return self.rolls[index] + self.rolls[index + 1] == self.MAX_PINS

    def _strike_bonus(self, index: int) -> int:
        return self.rolls[index + 1] + self.rolls[index + 2]

    def _spare_bonus(self, index: int) -> int:
        return self.rolls[index + 2]

    def _sum_of_balls_in_frame(self, index: int) -> int:
        return self.rolls[index] + self.rolls[index + 1]

    def _validate_game_complete(self) -> None:
        frame_index = 0

        for frame in range(self.TOTAL_FRAMES):

            if frame_index >= len(self.rolls):
                raise ValueError("Game is incomplete")

            if self._is_strike(frame_index):
                frame_index += 1

                if frame == 9:
                    if len(self.rolls) < frame_index + 2:
                        raise ValueError("Game is incomplete")

            else:
                if frame_index + 1 >= len(self.rolls):
                    raise ValueError("Game is incomplete")

                if self.rolls[frame_index] + self.rolls[frame_index + 1] > self.MAX_PINS:
                    raise ValueError("Invalid frame score")

                if self._is_spare(frame_index):
                    frame_index += 2

                    if frame == 9:
                        if len(self.rolls) < frame_index + 1:
                            raise ValueError("Game is incomplete")
                else:
                    frame_index += 2

        # ✅ Allow only valid bonus rolls (max 2)
        if len(self.rolls) > frame_index + 2:
            raise ValueError("Too many rolls in game")

    def _validate_game_state(self) -> None:
        frame_index = 0
        frame = 0

        while frame < 9 and frame_index < len(self.rolls):

            first = self.rolls[frame_index]

            if first == self.MAX_PINS:
                frame_index += 1

            else:
                if frame_index + 1 < len(self.rolls):
                    second = self.rolls[frame_index + 1]

                    if first + second > self.MAX_PINS:
                        raise ValueError("Invalid frame score")

                frame_index += 2

            frame += 1
