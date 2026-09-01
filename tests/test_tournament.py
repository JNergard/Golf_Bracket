"""Tests for golf_bracket.tournament."""
from golf_bracket.player import Player
from golf_bracket.pairing import make_pairing
from golf_bracket.tournament import record_match

def test_record_match():
    """Test the record_match function to ensure it correctly updates player records."""
    Player1 = Player(name="Player1", seed=10)
    Player2 = Player(name="Player2", seed=12)

    record_match(Player1, Player2)

    assert Player1.wins == 1
    assert Player1.losses == 0
    assert Player1.opponents == [Player2]
    assert Player1.eliminated is False

    assert Player2.wins == 0
    assert Player2.losses == 1
    assert Player2.opponents == [Player1]
    assert Player2.eliminated is False