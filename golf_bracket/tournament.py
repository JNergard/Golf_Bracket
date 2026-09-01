"""Tournament orchestration: rounds, elimination, result recording, overall state."""
from golf_bracket.player import Player
from golf_bracket.pairing import make_pairing
from dataclasses import dataclass, field

@dataclass
class Tournament:
    players: list[Player]
    round_num: int = 1
    match_history: list = field(default_factory=list)

    def record_match(self, winner: Player, loser: Player) -> None:
        """Record the result of a match between two players, updating their records accordingly."""
        winner.record_result(loser, won=True)
        loser.record_result(winner, won=False)
        self.match_history.append((self.round_num, winner, loser))

    def alive_players(self) -> list[Player]:
        alive = []
        for p in self.players:
            if not p.eliminated:
                alive.append(p)
        return alive

    