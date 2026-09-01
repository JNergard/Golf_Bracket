"""Round pairing logic: bucketing by record, fold pairing, rematch avoidance, pairing-down."""
from golf_bracket.player import Player
from collections import defaultdict


def bucket_by_record(players: list[Player]) -> dict[tuple[int, int], list[Player]]:
    buckets = defaultdict(list)
    for player in players:
        key = (player.wins, player.losses)
        buckets[key].append(player)

    return buckets


def fold_pair(players: list[Player]) -> list[tuple[Player, Player]]:
    """Make pairings for a round in the tournament by splitting players into two halves 
    and pairing the top half with the bottom half in reverse order."""
    sorted_players = sorted(players, key=lambda player: (-player.resistance, player.seed))

    half_len_list = len(sorted_players)//2
    first_half = sorted_players[:half_len_list]
    second_half = sorted_players[half_len_list:]
    second_half_reversed = second_half[::-1]

    pairings = list(zip(first_half, second_half_reversed))
    return pairings