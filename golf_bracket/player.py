"""Player class: identity, seed, record, and match history."""
from dataclasses import dataclass, field
@dataclass
class Player:
    name: str
    seed: int
    wins: int = 0
    losses: int = 0
    opponents: list = field(default_factory=list)

    def add_opponent(self, opponent: "Player") -> None:
        self.opponents.append(opponent)

    def record_result(self, opponent: "Player", won: bool) -> None:
        self.add_opponent(opponent)
        if won:
            self.wins += 1
            
        else:
            self.losses += 1
            

    @property
    def eliminated(self) -> bool:
        return self.losses > 1