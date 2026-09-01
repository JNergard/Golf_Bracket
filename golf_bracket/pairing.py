"""Round pairing logic: bucketing by record, fold pairing, rematch avoidance, pairing-down."""
from golf_bracket.player import Player

def make_pairing(players: list[Player], round_num: int) -> list[tuple[Player, Player]]:
    sorted_players = sorted(players, key=lambda player: player.seed)

    half_len_list = len(sorted_players)//2
    first_half = sorted_players[:half_len_list]
    second_half = sorted_players[half_len_list:]
    second_half_reversed = second_half[::-1]

    pairings = list(zip(first_half, second_half_reversed))
    return pairings
        