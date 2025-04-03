BASE_URL = "https://www.sports-reference.com"

YEARS = [ 2023, 2024 ]

REGIONS = [ "East", "Midwest", "South", "West", "National" ]

ROUNDS = ["First", "Second", "Sweet 16", "Elite 8", "Final 4", "National Championship"]

UNDERLINE_START = "\033[4m"

UNDERLINE_END = "\033[0m"

def get_bracket_url(year):
    return f"{BASE_URL}/cbb/postseason/men/{year}-ncaa.html"

def print_matchup(team_a, team_b, team_a_seed, team_b_seed, winner):
   print(f"({team_a_seed}) {UNDERLINE_START if winner == 0 else ""}{team_a}{UNDERLINE_END if winner == 0 else ""} - ({team_b_seed}) {UNDERLINE_START if winner == 1 else ""}{team_b}{UNDERLINE_END if winner == 1 else ""}")