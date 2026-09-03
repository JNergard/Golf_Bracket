"""Flask app to run bracket code on browser"""
import os
from golf_bracket.persistence import load_tournament_from_gh, save_tournament_to_github
from golf_bracket.player import Player
from golf_bracket.tournament import Tournament
from flask import Flask
from flask import request
from flask import redirect
import base64
import requests

app = Flask(__name__)

OWNER = "JNergard"
REPO = "Golf_Bracket"
PATH = "data/tournament.json"


def load_or_create_tournament() -> Tournament | None:
    token = os.environ["GITHUB_TOKEN"]
    try:
        return load_tournament_from_gh(OWNER, REPO, PATH, token)
    except requests.exceptions.HTTPError:
        return None


@app.route("/setup", methods=["POST"])
def setup():
    lines = request.form["player_names"]
    split_lines = [line.strip() for line in lines.splitlines() if line.strip()]

    players = []
    enumerated_players = enumerate(split_lines, start =1)
    for seed, name in enumerated_players:
        new_player = Player(name = name, seed = seed)
        players.append(new_player)

    tournament = Tournament(players=players)
    save_tournament_to_github(tournament, OWNER, REPO, PATH, os.environ["GITHUB_TOKEN"])
    return redirect("/")


#stylizations provided by claude code
PAGE_STYLE = """
<style>
  :root {
    --blue: #1d3f72;
    --blue-dark: #142b4e;
    --gold: #c8a544;
    --bg: #f7f7f5;
    --card: #ffffff;
    --text: #1a1a1a;
    --muted: #6b6b6b;
    --border: #e3e1db;
  }
  * { box-sizing: border-box; }
  body {
    margin: 0;
    background: var(--bg);
    color: var(--text);
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
  }
  .container {
    max-width: 480px;
    margin: 0 auto;
    padding: 0 0 3rem;
  }
  header {
    background: var(--blue);
    color: #fff;
    padding: 1.25rem 1rem 1rem;
    border-bottom: 3px solid var(--gold);
    text-align: center;
  }
  header h1 {
    margin: 0;
    font-size: 1.3rem;
    font-weight: 600;
    letter-spacing: 0.02em;
  }
  header p {
    margin: 0.25rem 0 0;
    color: #d9e0eb;
    font-size: 0.9rem;
  }
  section {
    padding: 1.25rem 1rem 0;
  }
  h2 {
    font-size: 1rem;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    color: var(--muted);
    margin: 0 0 0.75rem;
  }
  .card {
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 0.9rem 1rem;
    margin-bottom: 0.75rem;
    box-shadow: 0 1px 2px rgba(0,0,0,0.04);
  }
  .matchup {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 0.75rem;
  }
  .matchup .side {
    flex: 1;
    text-align: center;
  }
  .matchup .player-name {
    font-weight: 600;
  }
  .matchup .player-record {
    color: var(--muted);
    font-size: 0.85rem;
    margin-top: 0.15rem;
  }
  .matchup .vs {
    color: var(--muted);
    font-size: 0.8rem;
    padding: 0 0.5rem;
  }
  .win-buttons form {
    margin: 0;
  }
  .win-buttons {
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
  }
  .win-buttons form {
    display: block;
  }
  button {
    font: inherit;
    cursor: pointer;
    border-radius: 8px;
    border: none;
  }
  .win-buttons button {
    width: 100%;
    padding: 0.8rem 0.5rem;
    font-weight: 600;
    font-size: 0.95rem;
  }
  .win-buttons button.blue {
    background: var(--blue);
    color: #fff;
  }
  .win-buttons button.blue:active {
    background: var(--blue-dark);
  }
  .win-buttons button.gold {
    background: var(--gold);
    color: var(--blue-dark);
  }
  .win-buttons button.gold:active {
    background: #b3922f;
  }
  table {
    width: 100%;
    border-collapse: collapse;
    background: var(--card);
    border-radius: 10px;
    overflow: hidden;
    border: 1px solid var(--border);
  }
  th, td {
    padding: 0.55rem 0.6rem;
    text-align: right;
    font-size: 0.9rem;
  }
  th:first-child, td:first-child {
    text-align: left;
  }
  th {
    background: var(--blue);
    color: #fff;
    font-weight: 600;
  }
  tbody tr:nth-child(even) {
    background: #f0f1ee;
  }
  tbody tr:first-child td {
    border-left: 3px solid var(--gold);
  }
  .danger-zone {
    margin-top: 2rem;
    padding-top: 1rem;
    border-top: 1px solid var(--border);
  }
  .danger-zone form {
    display: inline-block;
    margin-right: 0.5rem;
  }
  .danger-zone button {
    padding: 0.5rem 0.9rem;
    background: transparent;
    color: var(--muted);
    border: 1px solid var(--border);
    font-size: 0.85rem;
  }
  .danger-zone button:active {
    background: #efece0;
  }
  .champion {
    text-align: center;
    padding: 3rem 1.5rem;
  }
  .champion .trophy-line {
    width: 48px;
    height: 3px;
    background: var(--gold);
    margin: 0 auto 1.5rem;
  }
  .champion h1 {
    font-size: 1.1rem;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    color: var(--muted);
    margin: 0 0 0.5rem;
  }
  .champion .name {
    font-size: 2rem;
    font-weight: 700;
    color: var(--blue);
  }
  .setup textarea {
    width: 100%;
    min-height: 260px;
    padding: 0.75rem;
    border: 1px solid var(--border);
    border-radius: 8px;
    font: inherit;
    font-size: 0.95rem;
    resize: vertical;
  }
  .setup .hint {
    color: var(--muted);
    font-size: 0.85rem;
    margin: 0.5rem 0 1rem;
  }
  .setup button {
    width: 100%;
    padding: 0.85rem;
    background: var(--blue);
    color: #fff;
    font-weight: 600;
    font-size: 1rem;
  }
  .setup button:active {
    background: var(--blue-dark);
  }
</style>
"""


def render_page(body: str) -> str:
    return f"""<!doctype html>
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Golf Bracket</title>
{PAGE_STYLE}
</head>
<body>
<div class="container">
{body}
</div>
</body>
</html>"""


def standings_table_html(tournament: Tournament) -> str:
    sorted_players = sorted(tournament.players, key=lambda p: (-p.wins, p.losses, p.seed))
    rows = "\n".join(
        f"<tr><td>{p.name}</td><td>{p.wins}</td><td>{p.losses}</td></tr>"
        for p in sorted_players
    )
    return f"""
    <section>
      <h2>Standings</h2>
      <table>
        <thead><tr><th>Name</th><th>W</th><th>L</th></tr></thead>
        <tbody>{rows}</tbody>
      </table>
    </section>
    """


def setup_form_html() -> str:
    return """
    <header><h1>Golf Bracket</h1></header>
    <section class="setup">
      <h2>Set Up Tournament</h2>
      <p class="hint">Enter each player's name, one per line. The order
      you list them in sets their seed for round 1 (first line plays
      last line, second line plays second-to-last, and so on).</p>
      <form method="post" action="/setup">
        <textarea name="player_names" placeholder="Alice&#10;Bob&#10;Carol&#10;..."></textarea>
        <button type="submit">Start Tournament</button>
      </form>
    </section>
    """


@app.route("/restart_tournament", methods=["POST"])
def restartTourney():
    tournament = load_or_create_tournament()
    tournament.restart_tournament()
    save_tournament_to_github(tournament, OWNER, REPO, PATH, os.environ["GITHUB_TOKEN"])
    return redirect("/")


@app.route("/restart_round", methods=["POST"])
def restartRound():
    tournament = load_or_create_tournament()
    tournament.restart_round()
    save_tournament_to_github(tournament, OWNER, REPO, PATH, os.environ["GITHUB_TOKEN"])
    return redirect("/")


@app.route("/record", methods=["POST"])
def record():
    winner_seed = int(request.form["winner_seed"])
    loser_seed = int(request.form["loser_seed"])

    tournament = load_or_create_tournament()

    players_by_seed = {p.seed: p for p in tournament.players}
    round_winner = players_by_seed[winner_seed]
    round_loser = players_by_seed[loser_seed]
    tournament.record_match(winner=round_winner, loser=round_loser)

    tournament.pending_pairings = [
        (a, b) for a, b in tournament.pending_pairings
        if {a.seed, b.seed} != {winner_seed, loser_seed}
    ]

    if not tournament.pending_pairings:
        tournament.round_num += 1

    save_tournament_to_github(tournament, OWNER, REPO, PATH, os.environ["GITHUB_TOKEN"])
    return redirect("/")


@app.route("/")
def startTourney():
    tournament = load_or_create_tournament()
    if tournament is None:
        return render_page(setup_form_html())
    

    if tournament.is_over:
        body = f"""
        <header><h1>Golf Bracket</h1></header>
        <div class="champion">
          <div class="trophy-line"></div>
          <h1>Champion</h1>
          <div class="name">{tournament.champion.name}</div>
        </div>
        """
        return render_page(body)

    tournament.start_round_if_needed()
    save_tournament_to_github(tournament, OWNER, REPO, PATH, os.environ["GITHUB_TOKEN"])

    matchup_cards = []
    for player_a, player_b in tournament.pending_pairings:
        matchup_cards.append(f"""
        <div class="card">
          <div class="matchup">
            <div class="side">
              <div class="player-name">{player_a.name}</div>
              <div class="player-record">{player_a.wins}-{player_a.losses}</div>
            </div>
            <div class="vs">vs</div>
            <div class="side">
              <div class="player-name">{player_b.name}</div>
              <div class="player-record">{player_b.wins}-{player_b.losses}</div>
            </div>
          </div>
          <div class="win-buttons">
            <form method="post" action="/record">
                <input type="hidden" name="winner_seed" value="{player_a.seed}">
                <input type="hidden" name="loser_seed" value="{player_b.seed}">
                <button type="submit" class="blue">{player_a.name} wins</button>
            </form>
            <form method="post" action="/record">
                <input type="hidden" name="winner_seed" value="{player_b.seed}">
                <input type="hidden" name="loser_seed" value="{player_a.seed}">
                <button type="submit" class="gold">{player_b.name} wins</button>
            </form>
          </div>
        </div>
        """)
    matchups_html = "\n".join(matchup_cards)

    body = f"""
    <header>
      <h1>Golf Bracket</h1>
      <p>Round {tournament.round_num}</p>
    </header>
    <section>
      <h2>Matchups</h2>
      {matchups_html}
    </section>
    {standings_table_html(tournament)}
    <section class="danger-zone">
      <form method="post" action="/restart_round">
          <button type="submit">Restart Round</button>
      </form>
      <form method="post" action="/restart_tournament">
          <button type="submit">Restart Tournament</button>
      </form>
    </section>
    """
    return render_page(body)


if __name__ == "__main__":
    app.run(debug=True)
