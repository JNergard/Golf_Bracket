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

    pairings = resolve_rematches(first_half, second_half_reversed)


    return pairings

def resolve_rematches(first_half: list[Player], second_half: list[Player]) -> list[tuple[Player, Player]]:
    second_half = list(second_half)  

    for i in range(len(first_half)):
        if second_half[i] in first_half[i].opponents:
            for j in range(i+1, len(second_half)):
                if second_half[j] not in first_half[i].opponents:
                    second_half[i], second_half[j] = second_half[j], second_half[i]
                    break

    return list(zip(first_half, second_half))


def round_pairings(players: list[Player]) -> list[tuple[Player, Player]]:
    pairings = []
    bucketed_players = bucket_by_record(players)
    for bucket in bucketed_players.values():
        pair = fold_pair(bucket)
        pairings.extend(pair)
        
    return pairings

def process_bucket(bucket: list[Player], carry: Player | None) -> tuple[list[tuple[Player, Player]], Player | None]:
    """Processes one bucket in worst-to-best order, absorbing an incoming carry if present, and producign an 
    outgoing carry if this bucket can't pair evenly."""
    pool = list(bucket)
    pairings = []

    if carry is not None:
        ranked = sorted(pool, key=lambda p: (-p.resistance, p.seed))
        pairings.append((carry, ranked[-1]))
        pool.remove(ranked[-1])
        carry = None

    if len(pool) % 2 == 1:
        ranked = sorted(pool, key=lambda p: (-p.resistance, p.seed))
        carry = ranked[-1]
        pool.remove(ranked[-1])

    pairings.extend(fold_pair(pool)) 
    return pairings, carry


    sorted(buckets.items(), key=lambda win_loss: (win_loss[0][0], -win_loss[0][1]))