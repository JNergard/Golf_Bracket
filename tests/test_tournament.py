"""Tests for golf_bracket.tournament."""
from golf_bracket.player import Player
from golf_bracket.persistence import load_tournament

import json
from golf_bracket.tournament import Tournament
from golf_bracket.persistence import save_tournament

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

def test_bye():
    Player1 = Player(name="Player1", seed=1, wins = 3, losses = 0)
    test_tourney = Tournament(players = [Player1])
    test_tourney.record_bye(Player1)
    assert Player1.opponents == []
    assert (1, Player1, None) in test_tourney.match_history

def test_tourney_end():
    Player1 = Player(name="Player1", seed=1, wins = 3, losses = 0)
    test_tourney = Tournament(players = [Player1])
    assert test_tourney.is_over == True
    assert test_tourney.champion == Player1


def test_json():
    Player1 = Player(name="Player1", seed=10)
    Player2 = Player(name="Player2", seed=12)
    
    test_tourney = Tournament(players = [Player1, Player2])
    test_tourney.start_round_if_needed()
    test_tourney.record_match(winner = Player1, loser = Player2)
    

    save_tournament(test_tourney, "test.json")
    with open("test.json") as f:
        data = json.load(f)

    assert len(data["players"]) == 2
    assert data["round_num"] == 1
    assert len(data["pending_pairings"]) == 1

def test_load():
    Player1 = Player(name="Player1", seed=10)
    Player2 = Player(name="Player2", seed=12)
    
    test_tourney = Tournament(players = [Player1, Player2])
    
    test_tourney.record_match(winner = Player1, loser = Player2)

    save_tournament(test_tourney, "test.json")
    
    
    loaded_tourney = load_tournament("test.json")

    loaded_player1 = next(p for p in loaded_tourney.players if p.seed == 10)
    assert loaded_player1.wins == 1
    assert loaded_player1.losses == 0
    assert len(loaded_player1.opponents) == 1
    assert loaded_player1.opponents[0].seed == 12

def test_start_round_if_needed():
    Player1 = Player(name="Player1", seed=1, wins = 3, losses = 0)
    Player2 = Player(name="Player2", seed=2, wins = 3, losses = 0)
    Player5 = Player(name="Player5", seed=5, wins = 1, losses = 2)
    Player6 = Player(name="Player6", seed=6, wins = 0, losses = 2)
    
    test_tourney = Tournament(players = [Player1, Player2, Player5, Player6])
    test_tourney.start_round_if_needed()
    first_call_pairings = test_tourney.pending_pairings
    test_tourney.start_round_if_needed()
    assert test_tourney.pending_pairings == first_call_pairings

def test_restart_tournament():
    Player1 = Player(name="Player1", seed=1, wins=3, losses=0)
    Player2 = Player(name="Player2", seed=2, wins=0, losses=2)

    test_tourney = Tournament(players=[Player1, Player2], round_num=3,
                               match_history=[(2, Player1, Player2)],
                               pending_pairings=[(Player1, Player2)])

    test_tourney.restart_tournament()

    assert Player1.wins == 0
    assert Player1.losses == 0
    assert Player1.opponents == []

    assert Player2.wins == 0
    assert Player2.losses == 0
    assert Player2.opponents == []

    assert test_tourney.round_num == 1
    assert test_tourney.match_history == []
    assert test_tourney.pending_pairings == []

def test_restart_round():
    Player1 = Player(name="Player1", seed=1)
    Player2 = Player(name="Player2", seed=2)
    Player3 = Player(name="Player3", seed=3)

    test_tourney = Tournament(players=[Player1, Player2, Player3])
    test_tourney.record_match(winner=Player1, loser=Player2)
    test_tourney.record_bye(Player3)
    test_tourney.pending_pairings = []

    test_tourney.restart_round()

    assert Player1.wins == 0
    assert Player1.losses == 0
    assert Player1.opponents == []

    assert Player2.wins == 0
    assert Player2.losses == 0
    assert Player2.opponents == []

    assert Player3.wins == 0
    assert Player3.opponents == []

    assert test_tourney.match_history == []
    assert test_tourney.pending_pairings == []