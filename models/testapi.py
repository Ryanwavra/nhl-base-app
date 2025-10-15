from utils.api_client import NHLApiClient

# Initialize the API client
client = NHLApiClient()

# Fetch and parse live scores
scores = client.get_parsed_scores()

# Display results
print("🏒 Live Game Scores:")
if scores:
    for s in scores:
        score_line = f"{s.away_team} {s.away_score} vs {s.home_team} {s.home_score}"
        status_line = f"{s.status}"
        if s.status == "LIVE":
            status_line += f" — Period {s.period}, {s.time_remaining} remaining"
        print(f"{score_line} — {status_line}")
else:
    print("No live scores available.")