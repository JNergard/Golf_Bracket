"""Bare-bones Flask demo for the Golf Bracket engine.

TEMPORARY scaffolding, written to unblock a demo under time pressure.
Reuses all the existing golf_bracket engine code (Tournament, pairing,
display, persistence) unchanged -- only this file is new. Intended to
be rewritten from scratch as a learning exercise later: no error
handling, no styling, everything in one file with inline HTML via
render_template_string instead of a real templates/ folder.
"""
import os

from flask import Flask, redirect, render_template_string, request, url_for

from golf_bracket.display import print_bracket, print_standings
from golf_bracket.pairing import round_pairings
from golf_bracket.persistence import load_tournament, save_tournament
from golf_bracket.player import Player
from golf_bracket.tournament import Tournament

SAVE_PATH = "data/tournament.json"

app = Flask(__name__)

if os.path.exists(SAVE_PATH):
    tournament = load_tournament(SAVE_PATH)
else:
    players = [Player(name=f"Player{i}", seed=i) for i in range(1, 21)]
    tournament = Tournament(players=players)

current_pairings = None  # matches still pending for the round in progress


def start_new_round():
    global current_pairings
    pairings, bye = round_pairings(tournament.alive_players())
    if bye is not None:
        tournament.record_bye(bye)
        save_tournament(tournament, SAVE_PATH)
    current_pairings = pairings


PAGE = """
<!doctype html>
<title>Golf Bracket</title>
<style>
  body { font-family: sans-serif; max-width: 700px; margin: 2rem auto; }
  li { margin-bottom: 0.5rem; }
  pre { background: #f0f0f0; padding: 1rem; overflow-x: auto; }
</style>
<h1>Golf Bracket</h1>

{% if tournament.is_over %}
  <h2>Champion: {{ tournament.champion.name }}</h2>
{% else %}
  <h2>Round {{ tournament.round_num }}</h2>
  {% if pairings %}
    <ul>
    {% for a, b in pairings %}
      <li>
        {{ a.name }} vs {{ b.name }}
        &mdash;
        <form method="post" action="{{ url_for('record') }}" style="display:inline">
          <input type="hidden" name="winner_seed" value="{{ a.seed }}">
          <input type="hidden" name="loser_seed" value="{{ b.seed }}">
          <button type="submit">{{ a.name }} wins</button>
        </form>
        <form method="post" action="{{ url_for('record') }}" style="display:inline">
          <input type="hidden" name="winner_seed" value="{{ b.seed }}">
          <input type="hidden" name="loser_seed" value="{{ a.seed }}">
          <button type="submit">{{ b.name }} wins</button>
        </form>
      </li>
    {% endfor %}
    </ul>
  {% else %}
    <p>No matches pending for this round.</p>
  {% endif %}
{% endif %}

<h2>Standings</h2>
<pre>{{ standings }}</pre>

<h2>Bracket History</h2>
<pre>{{ bracket }}</pre>
"""


@app.route("/")
def index():
    global current_pairings
    if not tournament.is_over and current_pairings is None:
        start_new_round()

    return render_template_string(
        PAGE,
        tournament=tournament,
        pairings=current_pairings,
        standings=print_standings(tournament.players),
        bracket=print_bracket(tournament.match_history),
    )


@app.route("/record", methods=["POST"])
def record():
    global current_pairings

    winner_seed = int(request.form["winner_seed"])
    loser_seed = int(request.form["loser_seed"])
    by_seed = {p.seed: p for p in tournament.players}

    tournament.record_match(winner=by_seed[winner_seed], loser=by_seed[loser_seed])
    save_tournament(tournament, SAVE_PATH)

    current_pairings = [
        (a, b) for a, b in current_pairings
        if a.seed not in (winner_seed, loser_seed)
    ]

    if not current_pairings:
        tournament.round_num += 1
        current_pairings = None  # next GET / will start the following round

    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)
