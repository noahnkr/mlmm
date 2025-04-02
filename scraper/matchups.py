import requests
import time
from bs4 import BeautifulSoup
from utils import YEARS, REGIONS, ROUNDS, BASE_URL, get_bracket_url

matchup_history = []

for year in YEARS:
    print(f"--- Scraping {year} Season ---")
    bracket_url = get_bracket_url(year)
    response = requests.get(bracket_url)
    soup = BeautifulSoup(response.content, "lxml")

    for region in REGIONS:
        print(f"--- Scraping {region} Region ---")
        bracket = soup.find("div", {"id": region.lower()})

        rounds = bracket.find_all("div", {"class": "round"})[:-1] # Remove last round, which is just the region winner

        bracket_rounds = ROUNDS[:-2] if region != "National" else ROUNDS[-2:]
        for round, round_name in zip(rounds, bracket_rounds):
            print(f"--- Scraping {round_name} Round ---")
            matchups = round.find_all("div")
            
            for matchup in matchups:
                teams = matchup.find_all("div")
                if len(teams) != 2: continue

                team_a = teams[0].find("a").text.strip()
                team_b = teams[1].find("a").text.strip()

                team_a_seed = int(teams[0].find("span").text.strip())
                team_b_seed = int(teams[1].find("span").text.strip())

                team_a_link = BASE_URL + teams[0].find("a")["href"]
                team_b_link = BASE_URL + teams[1].find("a")["href"]

                winner = 0 if "winner" in teams[0].get("class", []) else 1
                print(f"Scraped ({team_a_seed}) {team_a} - ({team_b_seed}) {team_b} | Winner: {winner}")
                matchup_history.append({
                    "region": region,
                    "round": round_name,
                    "team_a": team_a,
                    "team_b": team_b,
                    "team_a_seed": team_a_seed,
                    "team_b_seed": team_b_seed,
                    "team_a_link": team_a_link,
                    "team_b_link": team_b_link,
                    "winner": winner,
                })

print(matchup_history)