"""Flask app to run bracket code on browser"""
import os
from golf_bracket.persistence import load_tournament_from_gh, save_tournament_to_github
from golf_bracket.player import Player
from golf_bracket.tournament import Tournament
from golf_bracket.pairing import round_pairings
from golf_bracket.display import print_standings
from flask import Flask
from flask import request
from flask import redirect
import base64
import requests

app = Flask(__name__)

SAVE_PATH = "data/tournament.json"
OWNER = "JNergard"
REPO = "Golf_Bracket"
PATH = "data/tournament.json"

def load_or_create_tournament() -> Tournament:
    token = os.environ["GITHUB_TOKEN"]
    try:
        return load_tournament_from_gh(OWNER, REPO, PATH, token)
    except requests.exceptions.HTTPError:
        players = [Player(name=f"Player{i}", seed=i) for i in range(1, 21)]
        return Tournament(players=players)

    
@app.route("/record", methods=["POST"])
def record():
    winner_seed = int(request.form["winner_seed"])
    loser_seed = int(request.form["loser_seed"])

    tournament = load_or_create_tournament()

    players_by_seed = {p.seed: p for p in tournament.players}
    round_winner = players_by_seed[winner_seed]
    round_loser = players_by_seed[loser_seed]
    tournament.record_match(winner=round_winner,loser=round_loser)

    save_tournament_to_github(tournament, OWNER, REPO, PATH, os.environ["GITHUB_TOKEN"])
    return redirect("/")
    

@app.route("/")
def startTourney():
    tournament = load_or_create_tournament()

    pairings, bye = round_pairings(tournament.alive_players())

    lines = []
    for player_a, player_b in pairings:
        lines.append(f"""
        <div>
            {player_a.name} vs {player_b.name}
            <form method="post" action="/record" style="display:inline">
                <input type="hidden" name="winner_seed" value="{player_a.seed}">
                <input type="hidden" name="loser_seed" value="{player_b.seed}">
                <button type="submit">{player_a.name} wins</button>
            </form>
            <form method="post" action="/record" style="display:inline">
                <input type="hidden" name="winner_seed" value="{player_b.seed}">
                <input type="hidden" name="loser_seed" value="{player_a.seed}">
                <button type="submit">{player_b.name} wins</button>
            </form>
        </div>
        """)
    pairing_text = "\n".join(lines)

    return f"<pre>{print_standings(tournament.players)}</pre>{pairing_text}"
   

if __name__ == "__main__":
    app.run(debug=True)
