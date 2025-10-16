from utils.api_client import NHLApiClient
from models.live_scores_model import parse_live_scores, should_show_game

client = NHLApiClient()

def display_schedule():
    today_games = client.get_today_games()
    tomorrow_games = client.get_tomorrow_games()

    print("📅 Today’s Games:")
    if today_games:
        for g in today_games:
            local_time = client.convert_utc_to_local(g.start_time)
            print(f"{g.away_team} vs {g.home_team} — {g.status} — {local_time}")
    else:
        print("No games scheduled today.")

    print("\n📅 Tomorrow’s Games:")
    if tomorrow_games:
        for g in tomorrow_games:
            local_time = client.convert_utc_to_local(g.start_time)
            print(f"{g.away_team} vs {g.home_team} — {g.status} — {local_time}")
    else:
        print("No games scheduled tomorrow.")

def display_visible_scores():
    raw = client.get_live_scores()
    scores = parse_live_scores(raw)
    visible_scores = [s for s in scores if should_show_game(s)]

    print("\n🏒 Visible Game Scores:")
    if visible_scores:
        for s in visible_scores:
            score_line = f"{s.away_team} {s.away_score} vs {s.home_team} {s.home_score}"
            period_info = f"Period {s.period}" if s.period else ""
            print(f"{score_line} — {s.status} — {period_info}")
    else:
        print("No live or recently completed games available.")

if __name__ == "__main__":
    display_schedule()
    display_visible_scores()