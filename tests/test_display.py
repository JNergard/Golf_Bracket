"""Tests for golf_bracket.display"""
from golf_bracket.player import Player
#from golf_bracket.pairing import make_pairing
#from golf_bracket.tournament import record_match
from golf_bracket.display import print_standings
from golf_bracket.display import print_bracket

def test_print_standings():
    Player1 = Player(name="Player1", seed=1, wins = 3, losses = 0)
    Player2 = Player(name="Player2", seed=2, wins = 3, losses = 0)
    Player3 = Player(name="Player3", seed=3, wins = 2, losses = 1)
    Player4 = Player(name="Player4", seed=4, wins = 2, losses = 2)
    Player5 = Player(name="Player5", seed=5, wins = 1, losses = 2)
    Player6 = Player(name="Player6", seed=6, wins = 0, losses = 2)

    Players = [Player1, Player2, Player3, Player4, Player5, Player6]
    result = print_standings(Players)

    
    lines = result.split("\n")

    assert len(lines) == 7
    assert "Player1" in lines[1]
    assert "Player6" in lines[6]
    

def test_bracket():
    Player1 = Player(name="Player1", seed=1, wins = 3, losses = 0)
    Player2 = Player(name="Player2", seed=2, wins = 3, losses = 0)
    Player3 = Player(name="Player3", seed=3, wins = 2, losses = 1)
    Player4 = Player(name="Player4", seed=4, wins = 2, losses = 2)
    Player5 = Player(name="Player5", seed=5, wins = 1, losses = 2)
    Player6 = Player(name="Player6", seed=6, wins = 0, losses = 2)

    match_history = [
        (1, Player1, Player2),
        (1, Player3, Player4),
        (1, Player5, None), 
        (2, Player1, Player3),
    ]

    result = print_bracket(match_history)
    lines = result.split("\n")

    assert "  Player5 VS " in lines