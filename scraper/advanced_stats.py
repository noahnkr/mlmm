import requests
import csv
import pandas as pd
from bs4 import BeautifulSoup 
from utils import (
    YEARS, ADVANCED_TEAM_STATS, get_season_advanced_stats_url
)

matchups = pd.read_csv("data/matchups.csv")
tournament_teams = set()

# Collect a set of all tournament teams by year
for _, matchup in matchups.iterrows():
    for team_col in ["team_a", "team_b"]:
        year = matchup["year"]
        team = matchup[team_col]
        tournament_teams.add((year, team))

advanced_team_stats_history = []

for year in YEARS:
    print(f"--- Scraping {year} Season ---")
    season_url = get_season_advanced_stats_url(year)
    res = requests.get(season_url)
    soup = BeautifulSoup(res.content, "lxml")

    stats_table = soup.find("table", {"id": "adv_school_stats"})
    table_body = stats_table.find("tbody")
    team_rows = table_body.find_all("tr")
    for row in team_rows:
        if "class" in row.attrs and "thead" in row["class"]: continue # Skip sub-headers

        team = row.find("td", {"data-stat": "school_name"}).text.strip()
        if (year, team) not in tournament_teams: continue # Skip non-tournament teams

        print(f"--- Scraping {year} {team} Advanced Stats ---")
        advanced_team_stats = { "year": year, "team": team }
        for stat_name, stat_id in ADVANCED_TEAM_STATS.items():
            stat = float(
                row.find("td", {"data-stat": stat_id}).text.strip()
            )
            advanced_team_stats[stat_name] = stat
        
        print(advanced_team_stats)
        advanced_team_stats_history.append(advanced_team_stats)

with open("data/advanced_stats.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=advanced_team_stats_history[0].keys())
    writer.writeheader()
    writer.writerows(advanced_team_stats_history)