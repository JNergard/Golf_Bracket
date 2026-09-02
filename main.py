"""CLI entry point: run the tournament loop (advance rounds, enter results, show standings)."""

from golf_bracket.player import Player
from golf_bracket.tournament import Tournament
from golf_bracket.pairing import round_pairings
from golf_bracket.display import print_standings

def main():
    players = [Player(name=f"Player{i}", seed=i) for i in range(1, 21)]
    tournament = Tournament(players=players)

    while not tournament.is_over:
        pairings, bye = round_pairings(tournament.alive_players())

        for player_a, player_b in pairings:
            # your turn: print the matchup, loop until valid input (1 or 2),
            # map the choice to winner/loser, call tournament.record_match
            print(f"1) {player_a.name}")
            print(f"2) {player_b.name}")
            while True:
                choice = input ("Winner (1 or 2): ")
                if choice == "1" or choice == "2":
                    break
                print("1 or 2 only")
            if choice == "1":
                tournament.record_match(winner=player_a, loser = player_b)
            else:
                tournament.record_match(winner=player_b, loser = player_a)


        if bye is not None:
            print(f"{bye.name} gets the Bye!")
            tournament.record_bye(bye)

        tournament.round_num += 1
        print(print_standings(tournament.players))

    print(f"Champion: {tournament.champion.name}")

if __name__ == "__main__":
    main()
