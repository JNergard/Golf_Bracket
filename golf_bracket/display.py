"""Terminal output: standings table and round-by-round bracket/history view."""
from golf_bracket.player import Player

def print_standings(players: list[Player]) -> str:
    sorted_players = sorted(players, key=lambda p: (-p.wins, p.losses, p.seed))

    

    standings = [f"{'Name':<15}{'Seed':>6}{'W':>5}{'L':>5}"]
    for p in sorted_players:
        standings.append(f"{p.name:<15}{p.seed:>6}{p.wins:>5}{p.losses:>5}")
    return "\n".join(standings)

def print_bracket(match_history: list) -> str:
    lines = []
    last_round = None

    for round_num, winner, loser in match_history:
        if round_num != last_round:
            lines.append(f"Round {round_num}:")
            last_round = round_num

        loser_name = loser.name if loser is not None else ""
        lines.append(f"  {winner.name} VS {loser_name}")

    return "\n".join(lines)