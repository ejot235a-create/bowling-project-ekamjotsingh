from bowling_game import BowlingGame

game = BowlingGame()

# Example game:
# Strike, then 3 and 6, then all gutters
game.roll(10)
game.roll(3)
game.roll(6)

for _ in range(16):
    game.roll(0)

print("Final score:", game.score())
