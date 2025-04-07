import requests
import csv
import pandas as pd
from bs4 import BeautifulSoup 
from utils import (
    YEARS, BASIC_TEAM_STATS, ADVANCED_TEAM_STATS, get_season_stats_url
)

matchups = pd.read_csv("data/matchups.csv")
tournament_teams = set()
stats_history = []

# Collect a set of all tournament teams by year
for _, matchup in matchups.iterrows():
    for team_col in ["team_a", "team_b"]:
        year = matchup["year"]
        team = matchup[team_col]
        tournament_teams.add((year, team))

def collect_stats(year, basic_stats=True):
    stats = []

    stats_url = get_season_stats_url(year, basic_stats)
    res = requests.get(stats_url)
    soup = BeautifulSoup(res.content, "lxml")

    table_id = "basic_school_stats" if basic_stats else "adv_school_stats"
    stats_table = soup.find("table", {"id": table_id})
    table_body = stats_table.find("tbody")
    team_rows = table_body.find_all("tr")

    for row in team_rows:
        if "class" in row.attrs and "thead" in row["class"]: continue # Skip sub-headers

        team = row.find("td", {"data-stat": "school_name"}).text.strip()
        if (year, team) not in tournament_teams: continue # Skip non-tournament teams

        print(f"--- Scraping {year} {team} {"Basic" if basic_stats else "Advanced"} Stats ---")

        team_stats = { "year": year, "team": team }
        stat_items = BASIC_TEAM_STATS.items() if basic_stats else ADVANCED_TEAM_STATS.items()
        for stat_name, stat_id in stat_items:
            stat = float(
                row.find("td", {"data-stat": stat_id}).text.strip()
            )
            stats[stat_name] = stat
        
        print(team_stats)
        stats.append(team_stats)
    
    return stats
    
for year in YEARS:
    # Collect Basic & Advanced stats
    basic_stats = collect_stats(year, True)
    adv_stats = collect_stats(year, False)
    
    # Create lookup dict by (year, team)
    basic_lookup = {
        (entry["year"], entry["team"]): entry for entry in basic_stats
    }
    adv_lookup = {
        (entry["year"], entry["team"]): entry for entry in adv_stats
    }

    # Combine Basic & Advanced Stats into single dict
    keys = set(basic_lookup.keys()) & set(adv_lookup.keys())
    for k in keys:
        combined_stats = {}
        combined_stats.update(basic_lookup[k])
        combined_stats.update(adv_lookup[k])
        stats_history.append(combined_stats)

with open("data/stats.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=stats_history[0].keys())
    writer.writeheader()
    writer.writerows(stats_history)