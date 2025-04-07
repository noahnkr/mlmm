import requests
import csv
import pandas as pd
from bs4 import BeautifulSoup 
from utils import BASIC_TEAM_STATS

matchups = pd.read_csv("data/matchups.csv")
seen = set()

basic_team_stats_history = []

for _, matchup in matchups.iterrows():
    for team_col in ["team_a", "team_b"]:
        year = matchup["year"]
        team = matchup[team_col]
        team_link = matchup[f"{team_col}_link"]
        key = (year, team)

        if key in seen: continue # We have collected this team's stats already
        seen.add(key)
        print(f"--- Scraping {year} {team} Basic Stats ---")

        res = requests.get(team_link)
        soup = BeautifulSoup(res.content, "lxml")

        stats_table = soup.find("table", {"id": "season-total_per_game"})
        basic_team_stats = { "year": year, "team": team }
        for stat_name, stat_id in BASIC_TEAM_STATS.items():
            stat = float(
                stats_table.find("td", {"data-stat": stat_id}).text.strip()
            )
            basic_team_stats[stat_name] = stat

        print(basic_team_stats)
        basic_team_stats_history.append(basic_team_stats)

with open("data/basic_stats.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=basic_team_stats_history[0].keys())
    writer.writeheader()
    writer.writerows(basic_team_stats_history)