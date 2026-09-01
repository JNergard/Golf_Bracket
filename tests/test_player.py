"""Tests for golf_bracket.player."""
from golf_bracket.player import Player



def test_player1():
    Player1 = Player(name="Player1", seed=10)
    assert Player1.wins == 0
    assert Player1.losses == 0
    assert Player1.opponents == []
    assert Player1.eliminated is False

def test_player2():
    Player2 = Player(name="Player2", seed=12)
    assert Player2.wins == 0
    assert Player2.losses == 0
    assert Player2.opponents == []
    assert Player2.eliminated is False

def test_player1_win():
    Player1 = Player(name="Player1", seed=10)
    Player2 = Player(name="Player2", seed = 12)

    Player1.record_result(Player2, True)
    assert Player1.wins == 1
    assert Player1.opponents == [Player2]

def test_player1_elim():
    Player1 = Player(name="Player1", seed=10)
    Player2 = Player(name="Player2", seed = 12)

    Player1.record_result(Player2, False)
    assert Player1.eliminated == False
    Player1.record_result(Player2, False)

    assert Player1.losses == 2
    assert Player1.eliminated is True

