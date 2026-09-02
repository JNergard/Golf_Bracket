"""Save/load tournament state to and from JSON so a tournament can span multiple sessions."""
import json
from golf_bracket.player import Player
from golf_bracket.tournament import Tournament

def save_tournament(tournament: Tournament, filepath: str) -> None:
    players_data = []
    for player in tournament.players:
        
        players_data.append(
            {"name": player.name, 
            "seed": player.seed, 
            "wins": player.wins, 
            "losses": player.losses, 
            "opponent_seeds": [opponent.seed for opponent in player.opponents]})


    history_data = []
    for round_num, winner, loser in tournament.match_history:
        
        history_data.append({
            "round_num": round_num,
            "winner_seed": winner.seed,
            "loser_seed": loser.seed if loser is not None else None})
        

    data = {
        "round_num": tournament.round_num,
        "players": players_data,
        "match_history": history_data,
    }

    with open(filepath, "w") as f:
        json.dump(data, f)


def load_tournament(filepath: str) -> Tournament:
    with open(filepath) as f:
        data = json.load(f)

    players = []
    for player_data in data["players"]:
        players.append(Player(
            name=player_data["name"],
            seed=player_data["seed"],
            wins=player_data["wins"],
            losses=player_data["losses"],
        ))

    players_by_seed = {p.seed: p for p in players}
    for player_data, player in zip(data["players"], players):
        player.opponents = [players_by_seed[seed] for seed in player_data["opponent_seeds"]]

    match_history = []
    for entry in data["match_history"]:
        winner = players_by_seed[entry["winner_seed"]]
        # your turn: get `loser` the same way, but handle the None case
        loser = players_by_seed[entry["loser_seed"]] if entry["loser_seed"] is not None else None
        match_history.append((entry["round_num"], winner, loser))

    return Tournament(players=players, round_num=data["round_num"], match_history=match_history)