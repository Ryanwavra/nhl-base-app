from utils.api_client import NHLApiClient
from models.live_scores_model import parse_live_scores, should_show_game
from db import create_submission, add_pick, get_submissions


def display_schedule(client: NHLApiClient) -> None:
    """Print today's and tomorrow's NHL schedule."""
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


def display_visible_scores(client: NHLApiClient) -> None:
    """Print live or recently completed game scores."""
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


def collect_user_input():
    """Prompt the user for ID, picks, and tiebreaker guess."""
    user_id = input("Enter your user ID: ")
    tiebreaker = int(input("Enter your tiebreaker guess (total goals in highest scoring game): "))

    picks = []
    while True:
        game_id = input("Enter game ID (or 'done' to finish): ")
        if game_id.lower() == "done":
            break
        team = input(f"Pick winner for {game_id}: ")
        picks.append({"game_id": game_id, "picked_team": team})

    return user_id, tiebreaker, picks


def run_cli_submission():
    """Main CLI flow: collect picks and persist them to the database."""
    print("🏒 Welcome to the NHL Picks CLI 🏒")

    client = NHLApiClient()
    display_schedule(client)
    display_visible_scores(client)

    # Step 1: Collect input
    user_id, tiebreaker, picks = collect_user_input()

    # Step 2: Create submission in DB
    submission_id = create_submission(user_id, tiebreaker)
    print(f"\n✅ Submission created with ID {submission_id}")

    # Step 3: Store picks
    for pick in picks:
        add_pick(submission_id, pick["game_id"], pick["picked_team"])
    print(f"✅ Stored {len(picks)} picks for submission {submission_id}")

    # Step 4: Show all submissions (debug/confirmation)
    all_subs = get_submissions()
    print("\n📊 Current submissions in DB:")
    for sub in all_subs:
        print(sub)


if __name__ == "__main__":
    run_cli_submission()