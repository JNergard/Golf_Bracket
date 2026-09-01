"""Tests for golf_bracket.pairing."""
from golf_bracket.player import Player
from golf_bracket.pairing import fold_pair
from golf_bracket.pairing import bucket_by_record

def test_first_pairing():
    Players = [Player(name=f"Player{i}", seed=i) for i in range(1, 21)]
    
    first_pairing = fold_pair(Players)

    assert len(first_pairing) == 10
    assert first_pairing[0][0].seed == 1
    assert first_pairing[0][1].seed == 20
    assert first_pairing[-1][0].seed == 10
    assert first_pairing[-1][1].seed == 11

def test_bucketing():
    Player1 = Player(name="Player1", seed=1, wins = 3, losses = 0)
    Player2 = Player(name="Player2", seed=2, wins = 2, losses = 1)
    Player3 = Player(name="Player3", seed=3, wins = 3, losses = 0)
    ps = [Player1, Player2, Player3]

    assert bucket_by_record(ps) == {(3,0): [Player1, Player3], (2,1): [Player2]}