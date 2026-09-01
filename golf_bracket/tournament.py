"""Tournament orchestration: rounds, elimination, result recording, overall state."""
from golf_bracket.player import Player
from golf_bracket.pairing import make_pairing

def record_match(winner: Player, loser: Player) -> None:
    """Record the result of a match between two players, updating their records accordingly."""
    winner.record_result(loser, won=True)
    loser.record_result(winner, won=False)