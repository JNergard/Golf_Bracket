# Golf Bracket

A Swiss-style, 2-loss-cutoff match play tournament tracker for a 20-person golf team.

## Format

- 20 players, each given an initial seed 1-20.
- Round 1: seed-based fold pairing (1v20, 2v19, 3v18, ...).
- A player is eliminated on their 2nd loss (double-elimination cutoff).
- Every round after round 1: alive players are grouped into buckets by exact
  record (e.g. all 2-0 players, all 1-1 players). Within a bucket, players are
  ranked by `(resistance descending, seed ascending)` and fold-paired
  (top half vs bottom half), skipping any pairing that would be a rematch.
- Resistance = Buchholz score (sum of your opponents' current win totals),
  with initial seed as the tiebreak when Buchholz is equal. Before any games
  are played everyone's Buchholz is 0, which is why round 1 falls back to
  pure seed order automatically — same rule, no special case needed.
- Uneven buckets are handled by "pairing down": if a bucket can't pair
  internally (e.g. only 1 player), the excess flows *up* into the next
  bucket above, pulling out that bucket's weakest-ranked player (lowest
  resistance, seed as tiebreak) to face the orphaned player instead. This
  can cascade upward through multiple buckets. The bye, when the total
  number of alive players is odd, always lands on the single best-ranked
  player overall (highest resistance/seed) once the cascade resolves —
  the best player never has to play down a bucket, they just sit out.
  Not yet implemented (planned for Milestone 7); `pair_round` currently
  assumes every bucket has an even number of players.

## Project layout

```
golf_bracket/
  player.py       Player data model: identity, seed, record, match history
  resistance.py   Buchholz calculation
  pairing.py      Bucketing, fold pairing, rematch avoidance, pairing-down
  tournament.py   Orchestration: rounds, elimination, result recording
  display.py      Terminal standings table + bracket/history view
  persistence.py  Save/load tournament state as JSON
tests/            Unit tests, one file per module
main.py           CLI entry point
data/             Saved tournament JSON files
```

## Build order

1. `Player` data model
2. Round 1 pairing (seed fold)
3. Result recording + standings display
4. Buchholz calculation
5. Bucketing by record + elimination at 2 losses
6. Fold pairing within a bucket (Buchholz + seed, rematch-safe)
7. Pairing-down for uneven buckets
8. Tournament loop / CLI
9. Bracket/history view
10. Save/load (JSON)
