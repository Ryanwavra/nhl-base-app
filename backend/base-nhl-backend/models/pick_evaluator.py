from typing import Dict, List
from models.user_pick_model import UserSubmission
from models.live_scores_model import LiveScore

def evaluate_user_picks(
    submissions: Dict[str, UserSubmission],
    final_scores: List[LiveScore]
) -> Dict[str, int]:
    """
    Returns a dict of user_id → correct pick count
    """
    results = {}
    for user_id, submission in submissions.items():
        correct = 0
        for pick in submission.picks:
            for game in final_scores:
                if game.game_id == pick.game_id and game.status == "Done":
                    if game.home_score is not None and game.away_score is not None:
                        winner = game.home_team if game.home_score > game.away_score else game.away_team
                        if pick.picked_team == winner:
                            correct += 1
        results[user_id] = correct
    return results

def get_highest_scoring_game_total(final_scores: List[LiveScore]) -> int:
    """
    Returns the total goals in the highest scoring completed game
    """
    max_goals = 0
    for game in final_scores:
        if game.status == "Done" and game.home_score is not None and game.away_score is not None:
            total = game.home_score + game.away_score
            max_goals = max(max_goals, total)
    return max_goals

def resolve_tiebreaker(
    tied_users: List[UserSubmission],
    actual_total: int
) -> List[str]:
    """
    Returns a list of user_ids who guessed closest to the actual tiebreaker value
    """
    closest_diff = float("inf")
    winners = []

    for user in tied_users:
        diff = abs(user.tiebreaker_guess - actual_total)
        if diff < closest_diff:
            closest_diff = diff
            winners = [user.user_id]
        elif diff == closest_diff:
            winners.append(user.user_id)

    return winners