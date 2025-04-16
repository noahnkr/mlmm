BASE_URL = "https://www.sports-reference.com"

YEARS = [ 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2021, 2022, 2023, 2024, 2025 ]

REGIONS = [ "East", "Midwest", "South", "West", "National" ]

ROUNDS = [ "First", "Second", "Sweet 16", "Elite 8", "Final 4", "National Championship" ]

NUMERIC_STATS = {
    "FG": "fg",
    "FGA": "fga",
    "3P": "fg3",
    "3PA": "fg3a",
    "2P": "fg2",
    "2PA": "fg2a",
    "FT": "ft",
    "FTA": "fta",
    "ORB": "orb",
    "DRB": "drb",
    "TRB": "trb",
    "AST": "ast",
    "STL": "stl",
    "BLK": "blk",
    "TOV": "tov", 
    "PF": "pf", 
}

PERCENT_STATS = {
    "FG%": "fg_pct",
    "3P%": "fg3_pct",
    "2P%": "fg2_pct",
    "eFG%": "efg_pct",
    "FT%": "ft_pct",
}

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/122.0.0.0 Safari/537.36"
}

UNDERLINE_START = "\033[4m"

UNDERLINE_END = "\033[0m"

STATS_OUTPUT_PATH = "data/stats.csv"

MATCHUPS_OUTPUT_PATH = "data/matchups.csv"

def collect_tournament_teams(matchups):
    tournament_teams = []
    seen = set()
    for _, matchup in matchups.iterrows():
        for team_col in ["team_a", "team_b"]:
            year = matchup["year"]
            team = matchup[team_col]

            if (year, team) in seen:
                continue

            # Collects list of each tournament team for each year
            tournament_teams.append((year, team))
            seen.add((year, team))
    
    return tournament_teams

def get_bracket_url(year):
    return f"{BASE_URL}/cbb/postseason/men/{year}-ncaa.html"

def get_season_stats_url(year, team):
    return f"{BASE_URL}/cbb/schools/{team}/men/{year}-gamelogs.html"

def print_matchup(team_a, team_b, team_a_seed, team_b_seed, winner):
   print(f"({team_a_seed}) {UNDERLINE_START if winner == team_a else ""}{team_a}{UNDERLINE_END if winner == team_a else ""} vs. ({team_b_seed}) {UNDERLINE_START if winner == team_b else ""}{team_b}{UNDERLINE_END if winner == team_b else ""}")