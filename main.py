from utils.api_client import NHLApiClient
from models.live_scores_model import parse_live_scores, should_show_game
from models.user_pick_model import PickManager, UserPick
from db import create_submission, add_pick, get_submissions
from models.pick_evaluator import (
    evaluate_user_picks,
    get_highest_scoring_game_total,
    resolve_tiebreaker
)

#display game schedule
def display_schedule(client):
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

#display live and completed game scores
def display_visible_scores(client):
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

#Receive and store user input
def get_user_input(today_games):
    user_id = input("Enter your user ID: ")
    picks = []

    print("\nToday's Games:")
    for game in today_games:
        print(f"{game.game_id}: {game.away_team} @ {game.home_team}")
        team = input(f"Pick winner for {game.game_id}: ")
        picks.append(UserPick(game_id=game.game_id, picked_team=team))

    tiebreaker = int(input("Enter your tiebreaker guess (total goals in highest scoring game): "))
    return user_id, picks, tiebreaker

def submit_picks_to_db():
    client = NHLApiClient()
    pick_manager = PickManager()

    display_schedule(client)
    display_visible_scores(client)

    today_games = client.get_today_games()
    if not today_games:
        print("\nNo games today — skipping pick submission.")
        return

    user_id, picks, tiebreaker = get_user_input(today_games)
    success = pick_manager.submit_picks(user_id, picks, tiebreaker)

    if success:
        submission = pick_manager.get_submission(user_id)
        print("\n✅ Submission stored:")
        print(submission)
    else:
        print("\n❌ Submission failed. Please check your inputs.")

#evalute picks & choose winner
def evaluate_user_picks():
    client = NHLApiClient()
    pick_manager = PickManager()

    raw_scores = client.get_live_scores()
    final_scores = parse_live_scores(raw_scores)

    submissions = pick_manager.submissions
    if not submissions:
        print("⚠️ No user submissions found.")
        return

    results = evaluate_user_picks(submissions, final_scores)
    if not results:
        print("⚠️ No completed games to evaluate.")
        return

    max_correct = max(results.values())
    tied_users = [submissions[uid] for uid, score in results.items() if score == max_correct]

    if len(tied_users) > 1:
        actual_total = get_highest_scoring_game_total(final_scores)
        winners = resolve_tiebreaker(tied_users, actual_total)
        print(f"\n🏆 Tiebreaker Total: {actual_total}")
        print(f"🥇 Winner(s): {', '.join(winners)}")
    else:
        print(f"\n🥇 Winner: {tied_users[0].user_id}")

def collect_user_input():
    """Prompt the user for ID, picks, and tiebreaker."""
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

def run_db_submission():
    print("🏒 Welcome to the NHL Picks CLI 🏒")

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
