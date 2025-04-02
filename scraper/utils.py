BASE_URL = "https://www.sports-reference.com"

YEARS = [ 2023, 2024 ]

REGIONS = [ "East", "Midwest", "South", "West", "National" ]

ROUNDS = ["First", "Second", "Sweet 16", "Elite 8", "Final 4", "National Championship"]

def get_bracket_url(year):
    return f"{BASE_URL}/cbb/postseason/men/{year}-ncaa.html"