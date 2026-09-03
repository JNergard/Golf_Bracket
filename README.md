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
  Implemented in `round_pairings` (Milestone 7) via `process_bucket`,
  which threads a "carry" player through buckets ordered worst-to-best.
- A bye counts as a win (for standings and bucketing purposes), but does
  *not* get added to the player's opponent history — there's no real
  opponent, so it shouldn't factor into anyone's Buchholz score. One
  consequence: since the best player always gets the bye, and a bye win
  keeps them undefeated and alone at the top, the same player can end up
  receiving repeated byes over a tournament with a persistently odd
  number of alive players. Accepted tradeoff, not a bug.
- The tournament ends when exactly one alive player remains (everyone
  else has taken 2 losses) — that player is the champion.

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
11. Flask web app (`app.py`) for the coach, deployed to a free host
    (Render) with GitHub-API-based persistence instead of local disk
    (free hosts have ephemeral filesystems)

- `process_bucket`'s cross-bucket "carry" pairing also avoids rematches
  now, same idea as `resolve_rematches`: when absorbing an incoming
  carry, it searches from the worst-ranked player in the bucket upward
  for the first one who hasn't already played the carry, falling back
  to the original worst-ranked player (accepting the rematch) if nobody
  in the bucket is safe.
