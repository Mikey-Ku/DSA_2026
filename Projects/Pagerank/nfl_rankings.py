"""Rank the 2025 NFL teams with PageRank.

Each loss adds a link from the loser to the winner. The script prints the
regular-season rankings, then picks each playoff game with them, adding each
round's results before the next. It compares those picks with what happened.
Game data comes from github.com/nflverse/nfldata.
"""

import csv
from pathlib import Path

from pagerank import pagerank, top_pages


def load_games(filename):
    """Load every finished 2025 game from the CSV file."""
    games = []
    with open(filename, "r") as file:
        for row in csv.DictReader(file):
            # Keep only 2025 games that have a final score.
            if row["season"] != "2025" or row["home_score"] == "":
                continue

            home_score = int(row["home_score"])
            away_score = int(row["away_score"])

            # Skip ties, since there is no winner.
            if home_score == away_score:
                continue

            if home_score > away_score:
                winner, loser = row["home_team"], row["away_team"]
            else:
                winner, loser = row["away_team"], row["home_team"]
            games.append({"week": int(row["week"]), "type": row["game_type"], "winner": winner, "loser": loser})
    return games


def build_graph(games):
    """Build a graph where each loser links to the team that beat it."""
    graph = {}
    for game in games:
        # Make sure both teams exist in the dictionary.
        graph.setdefault(game["winner"], set())
        graph.setdefault(game["loser"], set())

        # A loss is a vote for the team that beat you.
        graph[game["loser"]].add(game["winner"])
    return graph


def records(games):
    """Count each team's wins and losses."""
    record = {}
    for game in games:
        record.setdefault(game["winner"], [0, 0])
        record.setdefault(game["loser"], [0, 0])
        record[game["winner"]][0] += 1
        record[game["loser"]][1] += 1
    return record


def win_percentages(games):
    """Calculate each team's win percentage."""
    percentages = {}
    for team, record in records(games).items():
        wins = record[0]
        losses = record[1]
        games_played = wins + losses
        percentages[team] = wins / games_played
    return percentages


ROUND_NAMES = {"WC": "Wild Card", "DIV": "Divisional", "CON": "Conference", "SB": "Super Bowl"}


def predict_playoffs(regular_season, playoffs):
    """Pick each playoff game by PageRank and by win %, adding each round's results before the next."""
    known_games = list(regular_season)
    picks = []
    for round_type in ROUND_NAMES:
        round_games = [game for game in playoffs if game["type"] == round_type]

        # Rank the teams with every game played so far.
        ranks, _ = pagerank(build_graph(known_games))
        percentages = win_percentages(known_games)
        for game in round_games:
            pagerank_pick = max(game["winner"], game["loser"], key=lambda team: ranks[team])
            win_pct_pick = max(game["winner"], game["loser"], key=lambda team: percentages[team])
            picks.append({"round": ROUND_NAMES[round_type], "game": game,
                          "pagerank_pick": pagerank_pick, "win_pct_pick": win_pct_pick})

        # Add this round's results before ranking for the next round.
        known_games += round_games
    return picks


if __name__ == "__main__":
    games = load_games(Path(__file__).parent / "nfl_data" / "games.csv")
    regular_season = [game for game in games if game["type"] == "REG"]
    playoffs = [game for game in games if game["type"] != "REG"]

    # Rank the teams with the whole regular season.
    season_ranks, _ = pagerank(build_graph(regular_season))
    season_record = records(regular_season)
    print("2025 PageRank rankings (regular season):")
    for place, (team, rank) in enumerate(top_pages(season_ranks, len(season_ranks)), start=1):
        wins, losses = season_record[team]
        print(f"{place}. {team}  PageRank {rank:.4f}  record {wins}-{losses}  win % {wins / (wins + losses):.3f}")

    # Pick the playoffs round by round, updating the rankings after each round.
    picks = predict_playoffs(regular_season, playoffs)
    print(f"\nPlayoff picks ({len(picks)} games):")
    for pick in picks:
        game = pick["game"]
        mark = "right" if pick["pagerank_pick"] == game["winner"] else "wrong"
        print(f"  {pick['round']:<11} {game['winner']} beat {game['loser']:<4} PageRank picked {pick['pagerank_pick']:<4} {mark}"
              f"  (win % picked {pick['win_pct_pick']})")
    pagerank_right = sum(pick["pagerank_pick"] == pick["game"]["winner"] for pick in picks)
    win_pct_right = sum(pick["win_pct_pick"] == pick["game"]["winner"] for pick in picks)
    print(f"\nPageRank: {pagerank_right} of {len(picks)} right ({pagerank_right / len(picks):.0%})")
    print(f"Win %: {win_pct_right} of {len(picks)} right ({win_pct_right / len(picks):.0%})")
