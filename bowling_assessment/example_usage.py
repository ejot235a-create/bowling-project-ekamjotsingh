from bowling_game import BowlingGame


def play_sample_game():
    game = BowlingGame()

    # Simulating a simple game:
    # First roll is a strike
    game.roll(10)

    # Next frame
    game.roll(3)
    game.roll(6)

    # Remaining rolls are all gutter balls
    for _ in range(16):
        game.roll(0)

    print("Calculated Score:", game.score())


if __name__ == "__main__":
    play_sample_game()
