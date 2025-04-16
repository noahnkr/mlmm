import time
import random
import csv
import requests
import pandas as pd
from bs4 import BeautifulSoup
from scraper.utils import (
    NUMERIC_STATS, PERCENT_STATS, STATS_OUTPUT_PATH,
    collect_tournament_teams, get_season_stats_url,
)

def parse_game(game_row):
    game_type = game_row.find("td", {"data-stat": "game_type"}).text.strip()
    if "REG" not in game_type and "CTOURN" not in game_type:
        return None

    game_stats = {}
    for stat_name, stat_id in NUMERIC_STATS.items():
        try:
            game_stats[stat_name] = int(game_row.find("td", {"data-stat": stat_id}).text.strip())
            game_stats[f"OPP_{stat_name}"] = int(game_row.find("td", {"data-stat": f"opp_{stat_id}"}).text.strip())
        except ValueError:
            continue

    for stat_name, stat_id in PERCENT_STATS.items():
        try:
            game_stats[stat_name] = float(game_row.find("td", {"data-stat": stat_id}).text.strip())
            game_stats[f"OPP_{stat_name}"] = float(game_row.find("td", {"data-stat": f"opp_{stat_id}"}).text.strip())
        except ValueError:
            continue

    return game_stats

def normalize_game_stats(team_stats, games):
    if len(games) == 0:
        return None

    df = pd.DataFrame(games)

    for stat in NUMERIC_STATS:
        team_stats[stat] = round(df[stat].sum() / len(games), 2)
        team_stats[f"OPP_{stat}"] = round(df[f"OPP_{stat}"].sum() / len(games), 2)

    for stat in PERCENT_STATS:
        team_stats[stat] = round(df[stat].mean(), 2)
        team_stats[f"OPP_{stat}"] = round(df[f"OPP_{stat}"].mean(), 2)

def collect_team_stats(year, team, stats_url,):
    team_stats = { "year": year, "team": team }
    res = requests.get(stats_url)
    time.sleep(random.uniform(3.0, 4.0))
    soup = BeautifulSoup(res.content, "lxml")

    # Grab SRS & SOS from team summary box
    info_stats = soup.select("div[data-template='Partials/Teams/Summary'] p")
    for info in info_stats:
        if "SRS" in info.text:
            team_stats["SRS"] = float(info.text.strip().split()[1])
        elif "SOS" in info.text:
            team_stats["SOS"] = float(info.text.strip().split()[1])

    stats_table = soup.find("table", {"class": "stats_table"})
    game_rows = stats_table.find("tbody").find_all("tr")

	# Aggregate non-tournament game stats
    game_history = []
    for row in game_rows:
        if "class" in row.attrs and "thead" in row["class"]:
            continue
        parsed = parse_game(row)
        if parsed:
            game_history.append(parsed)

	# Normalize numeric stats (FG, ORB, ...) and take average of percent stats (FG%, FT%, ...)
    normalize_game_stats(team_stats, game_history)

    return team_stats

matchups = pd.read_csv("data/matchups.csv")
tournament_teams = collect_tournament_teams(matchups)
stats_history = []

for year, team in tournament_teams:
	print(f"--- Scraping {year} {team} Stats ---")
	stats_url = get_season_stats_url(year, team)
	team_stats = collect_team_stats(year, team, stats_url)
	stats_history.append(team_stats)

print("--- Success! ---")

with open(STATS_OUTPUT_PATH, "w", newline="", encoding="utf-8") as f:
	writer = csv.DictWriter(f, fieldnames=stats_history[0].keys())
	writer.writeheader()
	for row in stats_history:
		writer.writerow(row)
