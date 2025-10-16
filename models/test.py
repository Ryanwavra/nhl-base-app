from models.user_pick_model import UserPick, UserSubmission
from models.live_scores_model import LiveScore
from models.pick_evaluator import (
    evaluate_user_picks,
    get_highest_scoring_game_total,
    resolve_tiebreaker
)

def mock_final_scores():
    return [
        LiveScore(
            game_id="20251015-TOR-DET",
            home_team="DET",
            away_team="TOR",
            home_score=3,
            away_score=5,
            status="Done",
            period="Final"
        ),
        LiveScore(
            game_id="20251015-BOS-NYR",
            home_team="BOS",
            away_team="NYR",
            home_score=2,
            away_score=2,
            status="Done",
            period="Final"
        ),
        LiveScore(
            game_id="20251015-SEA-VAN",
            home_team="SEA",
            away_team="VAN",
            home_score=6,
            away_score=4,
            status="Done",
            period="Final"
        )
    ]

def mock_submissions():
    return {
        "ryan123": UserSubmission(
            user_id="ryan123",
            picks=[
                UserPick(game_id="20251015-TOR-DET", picked_team="TOR"),
                UserPick(game_id="20251015-BOS-NYR", picked_team="NYR"),
                UserPick(game_id="20251015-SEA-VAN", picked_team="SEA")
            ],
            tiebreaker_guess=10,
            timestamp="2025-10-15T20:00:00Z"
        ),
        "alex456": UserSubmission(
            user_id="alex456",
            picks=[
                UserPick(game_id="20251015-TOR-DET", picked_team="DET"),
                UserPick(game_id="20251015-BOS-NYR", picked_team="NYR"),
                UserPick(game_id="20251015-SEA-VAN", picked_team="VAN")
            ],
            tiebreaker_guess=12,
            timestamp="2025-10-15T20:05:00Z"
        )
    }

def test_pick_evaluation():
    scores = mock_final_scores()
    submissions = mock_submissions()

    # Step 1: Evaluate correct picks
    results = evaluate_user_picks(submissions, scores)
    print("✅ Correct Picks Per User:")
    for user_id, correct in results.items():
        print(f"{user_id}: {correct}")

    # Step 2: Find top scorers
    max_correct = max(results.values())
    tied_users = [submissions[uid] for uid, score in results.items() if score == max_correct]

    # Step 3: Tiebreaker logic
    if len(tied_users) > 1:
        actual_total = get_highest_scoring_game_total(scores)
        winners = resolve_tiebreaker(tied_users, actual_total)
        print(f"\n🏆 Tiebreaker Total: {actual_total}")
        print(f"🥇 Winner(s): {winners}")
    else:
        print(f"\n🥇 Winner: {tied_users[0].user_id}")

if __name__ == "__main__":
    test_pick_evaluation()