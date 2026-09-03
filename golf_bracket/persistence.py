"""Save/load tournament state to and from JSON so a tournament can span multiple sessions."""
import json
from golf_bracket.player import Player
from golf_bracket.tournament import Tournament
import base64
import requests

def tournament_to_dict(tournament: Tournament) -> dict:
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
        "pending_pairings": [(a.seed, b.seed) for a, b in tournament.pending_pairings]
    }

    return data


def save_tournament(tournament: Tournament, filepath: str) -> None:

    data = tournament_to_dict(tournament)
    with open(filepath, "w") as f:
        json.dump(data, f)


def load_tournament(filepath: str) -> Tournament:
    with open(filepath) as f:
        data = json.load(f)
    tourney = dict_to_tournament(data)
    return tourney


def dict_to_tournament(data: dict) -> Tournament:
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

    pending_pairings = [
    (players_by_seed[a_seed], players_by_seed[b_seed])
    for a_seed, b_seed in data["pending_pairings"]]
    
    match_history = []
    for entry in data["match_history"]:
        winner = players_by_seed[entry["winner_seed"]]
            
        loser = players_by_seed[entry["loser_seed"]] if entry["loser_seed"] is not None else None
        match_history.append((entry["round_num"], winner, loser))
    
    return Tournament(players=players, round_num=data["round_num"], match_history=match_history, 
                      pending_pairings=pending_pairings)


def load_tournament_from_gh(owner: str, repo: str, path: str, token: str) -> Tournament:
    url = f"https://api.github.com/repos/{owner}/{repo}/contents/{path}"
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json",
    }

    response = requests.get(url, headers=headers)
    response.raise_for_status()
    response_data = response.json()
    content_b64 = response_data["content"]
    content_json = base64.b64decode(content_b64).decode()
    tournament = dict_to_tournament(json.loads(content_json))
    return tournament


def save_tournament_to_github(tournament: Tournament, owner: str, repo: str, path: str, token: str) -> None:
    url = f"https://api.github.com/repos/{owner}/{repo}/contents/{path}"
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json",
    }

    
    get_response = requests.get(url, headers=headers)
    sha = get_response.json()["sha"] if get_response.status_code == 200 else None

    
    data = tournament_to_dict(tournament)
    content_json = json.dumps(data)
    content_b64 = base64.b64encode(content_json.encode()).decode()

    
    payload = {"message": "Updating tournament status", "content": content_b64}
    if sha is not None:
        payload["sha"] = sha
    result = requests.put(url, headers=headers, json=payload)
    result.raise_for_status()
    