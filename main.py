from utils.api_client import NHLApiClient



# Initialize the API client
client = NHLApiClient()

# Fetch today's and tomorrow's games
today_games = client.get_today_games()
tomorrow_games = client.get_tomorrow_games()

# Display today's games
print("📅 Today’s Games:")
if today_games:
    for g in today_games:
        local_time = client.convert_utc_to_local(g.start_time)
        print(f"{g.away_team} vs {g.home_team} — {g.status} — {local_time}")
else:
    print("No games scheduled today.")

# Display tomorrow's games
print("\n📅 Tomorrow’s Games:")
if tomorrow_games:
    for g in tomorrow_games:
        local_time = client.convert_utc_to_local(g.start_time)
        print(f"{g.away_team} vs {g.home_team} — {g.status} — {local_time}")
else:
    print("No games scheduled tomorrow.")