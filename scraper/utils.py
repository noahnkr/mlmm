BASE_URL = "https://www.sports-reference.com"

YEARS = [ 2023, ]

REGIONS = [ "East", "Midwest", "South", "West", "National" ]

ROUNDS = ["First", "Second", "Sweet 16", "Elite 8", "Final 4", "National Championship"]

BASIC_TEAM_STATS = {
    "2P": "fg2_per_g", 
    "2PA": "fg2a_per_g", 
    "3P": "fg3_per_g", 
    "3PA": "fg3a_per_g", 
    "FT": "ft_per_g", 
    "FTA": "fta_per_g", 
    "ORB": "orb_per_g", 
    "DRB": "drb_per_g", 
    "AST": "ast_per_g", 
    "STL": "stl_per_g", 
    "BLK": "blk_per_g", 
    "TOV": "tov_per_g", 
    "PF": "pf_per_g", 
    "PTS": "pts_per_g",
}

ADVANCED_TEAM_STATS = {
   "W-L%": "win_loss_pct", 
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

UNDERLINE_START = "\033[4m"

UNDERLINE_END = "\033[0m"

def get_bracket_url(year):
    return f"{BASE_URL}/cbb/postseason/men/{year}-ncaa.html"

def get_season_stats_url(year, basic_stats):
    return f"{BASE_URL}/cbb/seasons/men/{year}-{"" if basic_stats else "advanced-"}school-stats.html"

def print_matchup(team_a, team_b, team_a_seed, team_b_seed, winner):
   print(f"({team_a_seed}) {UNDERLINE_START if winner == 0 else ""}{team_a}{UNDERLINE_END if winner == 0 else ""} - ({team_b_seed}) {UNDERLINE_START if winner == 1 else ""}{team_b}{UNDERLINE_END if winner == 1 else ""}")