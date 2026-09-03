"""Tests for golf_bracket.pairing."""
from golf_bracket.player import Player
from golf_bracket.pairing import fold_pair
from golf_bracket.pairing import bucket_by_record
from golf_bracket.pairing import round_pairings
from golf_bracket.pairing import resolve_rematches
from golf_bracket.pairing import process_bucket

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

def test_round_pairings():
    
    Player1 = Player(name="Player1", seed=1, wins=2, losses=0)
    Player2 = Player(name="Player2", seed=2, wins=2, losses=0)
    
    Player3 = Player(name="Player3", seed=3, wins=1, losses=1)
    Player4 = Player(name="Player4", seed=4, wins=1, losses=1)

    players = [Player1, Player2, Player3, Player4]
    pairings, bye = round_pairings(players)

    assert len(pairings) == 2
    assert (Player1, Player2) in pairings
    assert (Player3, Player4) in pairings
    assert bye == None

def test_resolve_rematches():
    A = Player(name="A", seed = 1)
    B = Player(name="B", seed = 2)
    C = Player(name="C", seed = 3) 
    D = Player(name="D", seed = 4)

    A.add_opponent(D)
    D.add_opponent(A)

    first_half = [A, B]
    second_half_reversed = [D, C]

    pairings = resolve_rematches(first_half, second_half_reversed)

    assert (A, C) in pairings
    assert (B, D) in pairings

def test_process_bucket_cascade():
    Seed1 = Player(name="Seed1", seed=1, wins=7, losses=0)
    Seed2 = Player(name="Seed2", seed=2, wins=7, losses=0)
    Seed3 = Player(name="Seed3", seed=3, wins=6, losses=1)

    bottom_pairings, carry = process_bucket([Seed3], None)

    top_pairings, final_carry = process_bucket([Seed1, Seed2], carry)

    assert bottom_pairings == []
    assert carry == Seed3
    assert (Seed3, Seed2) in top_pairings
    assert final_carry == Seed1

def test_process_bucket_carry_avoids_rematch():
    Player1 = Player(name="Player1", seed=1)
    Player2 = Player(name="Player2", seed=2)
    Player3 = Player(name="Player3", seed=3)

    Player2.add_opponent(Player3)
    Player3.add_opponent(Player2)

    pairings, carry = process_bucket([Player1, Player2], Player3)

    assert (Player3, Player1) in pairings
    assert carry == Player2

def test_process_bucket_carry_accepts_rematch_if_no_alternative():
    Player2 = Player(name="Player2", seed=2)
    Player3 = Player(name="Player3", seed=3)

    Player2.add_opponent(Player3)
    Player3.add_opponent(Player2)

    pairings, carry = process_bucket([Player2], Player3)

    assert (Player3, Player2) in pairings
    assert carry is None


    