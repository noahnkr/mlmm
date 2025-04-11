BASE_URL = "https://www.sports-reference.com"

YEARS = [ 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2021, 2022, 2023, 2024, 2025 ]

REGIONS = [ "East", "Midwest", "South", "West", "National" ]

ROUNDS = [ "First", "Second", "Sweet 16", "Elite 8", "Final 4", "National Championship" ]

BASIC_TEAM_STATS = {
    "GP": "g",
    "W-L%": "win_loss_pct", 
    "FG": "fg",
    "FGA": "fga",
    "FG%": "fg_pct",
    "3P": "fg3",
    "3PA": "fg3a",
    "3P%": "fg3_pct",
    "FT": "ft",
    "FTA": "fta",
    "FT%": "ft_pct",
    "ORB": "orb",
    "TRB": "trb",
    "AST": "ast",
    "STL": "stl",
    "BLK": "blk",
    "TOV": "tov", 
    "PF": "pf", 
}

ADVANCED_TEAM_STATS = {
   "SRS": "srs",
   "SOS": "sos", 
   "Pace": "pace",
   "ORtg": "off_rtg",
   "FTr": "fta_per_fga_pct",
   "3PAr": "fg3a_per_fga_pct",
   "TS%": "ts_pct",
   "TRB%": "trb_pct",
   "AST%": "ast_pct",
   "STL%": "stl_pct",
   "BLK%": "blk_pct",
   "eFG%": "efg_pct",
   "TOV%": "tov_pct",
   "ORB%": "orb_pct",
   "FT/FGA": "ft_rate",
}

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/122.0.0.0 Safari/537.36"
}

UNDERLINE_START = "\033[4m"

UNDERLINE_END = "\033[0m"

def get_bracket_url(year):
    return f"{BASE_URL}/cbb/postseason/men/{year}-ncaa.html"

def get_season_stats_url(year, basic_stats):
    return f"{BASE_URL}/cbb/seasons/men/{year}-{"" if basic_stats else "advanced-"}school-stats.html"

def print_matchup(team_a, team_b, team_a_seed, team_b_seed, winner):
   print(f"({team_a_seed}) {UNDERLINE_START if winner == team_a else ""}{team_a}{UNDERLINE_END if winner == team_a else ""} vs. ({team_b_seed}) {UNDERLINE_START if winner == team_b else ""}{team_b}{UNDERLINE_END if winner == team_b else ""}")