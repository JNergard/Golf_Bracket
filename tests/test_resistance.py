"""Tests for golf_bracket.resistance."""
from golf_bracket.player import Player

def test_resistance():
    Player1 = Player(name="Player1", seed=1, wins = 3, losses = 0)
    Player2 = Player(name="Player2", seed=2, wins = 2, losses = 1)
    Player3 = Player(name="Player3", seed=3, wins = 1, losses = 2)

    Player1.add_opponent(Player2)
    Player1.add_opponent(Player3)
    Player2.add_opponent(Player1)
    Player2.add_opponent(Player3)
    Player3.add_opponent(Player1)
    Player3.add_opponent(Player2)

    assert Player1.resistance == 3
    assert Player2.resistance == 4
    assert Player3.resistance == 5