"""Tests for golf_bracket.tournament."""
from golf_bracket.player import Player


from golf_bracket.tournament import Tournament

def test_record_match():
    """Test the record_match function to ensure it correctly updates player records."""
    Player1 = Player(name="Player1", seed=10)
    Player2 = Player(name="Player2", seed=12)

    test_tourney = Tournament(players = [Player1, Player2])

    test_tourney.record_match(winner = Player1, loser = Player2)
    assert Player1.wins == 1
    assert Player1.losses == 0
    assert Player1.opponents == [Player2]
    assert Player1.eliminated is False

    assert Player2.wins == 0
    assert Player2.losses == 1
    assert Player2.opponents == [Player1]
    assert Player2.eliminated is False

    assert test_tourney.match_history == [(1, Player1, Player2)]

def test_alive_players():
    Player1 = Player(name="Player1", seed=1, wins = 3, losses = 0)
    Player2 = Player(name="Player2", seed=2, wins = 3, losses = 0)
    Player5 = Player(name="Player5", seed=5, wins = 1, losses = 2)
    Player6 = Player(name="Player6", seed=6, wins = 0, losses = 2)

    test_tourney = Tournament(players = [Player1, Player2, Player5, Player6])

    assert test_tourney.alive_players() == [Player1, Player2]