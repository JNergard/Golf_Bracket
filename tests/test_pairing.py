"""Tests for golf_bracket.pairing."""
from golf_bracket.player import Player
from golf_bracket.pairing import make_pairing

def test_first_pairing():
    Players = [Player(name=f"Player{i}", seed=i) for i in range(1, 21)]
    
    first_pairing = make_pairing(Players, 1)

    assert len(first_pairing) == 10
    assert first_pairing[0][0].seed == 1
    assert first_pairing[0][1].seed == 20
    assert first_pairing[-1][0].seed == 10
    assert first_pairing[-1][1].seed == 11