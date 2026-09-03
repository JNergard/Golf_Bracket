"""Tournament orchestration: rounds, elimination, result recording, overall state."""
from golf_bracket.player import Player
from golf_bracket.pairing import fold_pair, round_pairings
from dataclasses import dataclass, field


@dataclass
class Tournament:
    players: list[Player]
    round_num: int = 1
    match_history: list = field(default_factory=list)
    pending_pairings: list = field(default_factory=list)

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

    def record_bye(self, player: Player) -> None:
        player.record_bye()
        self.match_history.append((self.round_num, player, None))

    @property
    def is_over(self) ->  bool:
        return len(self.alive_players()) == 1

    @property
    def champion(self) -> Player | None:
        if self.is_over:
            return self.alive_players()[0]

    def start_round_if_needed(self) -> None:
        if self.pending_pairings or self.is_over:
            return
        pairings, bye = round_pairings(self.alive_players())
        if bye is not None:
            self.record_bye(bye)
        self.pending_pairings = pairings
        


    