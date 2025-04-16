import time
import random
import csv
import requests
from bs4 import BeautifulSoup 
from scraper.utils import (
	YEARS, REGIONS, ROUNDS, HEADERS,
	get_bracket_url, print_matchup
)

matchup_history = []

for year in YEARS:
	print(f"--- Scraping {year} Season ---")
	bracket_url = get_bracket_url(year)
	res = requests.get(bracket_url, headers=HEADERS)
	time.sleep(random.uniform(2.0, 5.0)) # Avoid rate limiting
	soup = BeautifulSoup(res.content, "lxml")

	for region in REGIONS:
		print(f"--- Scraping {region} Region ---")
		bracket = soup.find("div", {"id": region.lower()}) # Region id is lowercase

		rounds = bracket.find_all("div", {"class": "round"})[:-1] # Remove last round, which is just the region winner
		bracket_rounds = ROUNDS[:-2] if region != "National" else ROUNDS[-2:]
		for round, round_name in zip(rounds, bracket_rounds):
			print(f"--- Scraping {round_name} Round ---")

			matchups = round.find_all("div")
			for matchup in matchups:
				teams = matchup.find_all("div")
				if len(teams) != 2: 
					continue

				team_a = teams[0].find("a")["href"].split("/")[3]
				team_b = teams[1].find("a")["href"].split("/")[3]

				team_a_seed = int(teams[0].find("span").text.strip())
				team_b_seed = int(teams[1].find("span").text.strip())

				winner = team_a if "winner" in teams[0].get("class", []) else team_b

				print_matchup(team_a, team_b, team_a_seed, team_b_seed, winner)
				matchup_history.append({
					"year": year,
					"region": region,
					"round": round_name,
					"team_a": team_a,
					"team_b": team_b,
					"team_a_seed": team_a_seed,
					"team_b_seed": team_b_seed,
					"winner": winner,
				})

print("--- Success! ---")

with open("data/matchups.csv", "w", newline="", encoding="utf-8") as f:
	writer = csv.DictWriter(f, fieldnames=matchup_history[0].keys())
	writer.writeheader()
	writer.writerows(matchup_history)