from dataclasses import dataclass
from typing import List, Dict, Optional
from datetime import datetime

@dataclass
class UserPick:
    game_id: str
    picked_team: str  # e.g. "TOR"

@dataclass
class UserSubmission:
    user_id: str
    picks: List[UserPick]
    tiebreaker_guess: int
    timestamp: str  # ISO format

class PickManager:
    def __init__(self):
        self.submissions: Dict[str, UserSubmission] = {}

    def submit_picks(self, user_id: str, picks: List[UserPick], tiebreaker_guess: int) -> bool:
        if not picks or tiebreaker_guess < 0:
            return False  # Basic validation

        timestamp = datetime.utcnow().isoformat()
        self.submissions[user_id] = UserSubmission(
            user_id=user_id,
            picks=picks,
            tiebreaker_guess=tiebreaker_guess,
            timestamp=timestamp
        )
        return True

    def get_submission(self, user_id: str) -> Optional[UserSubmission]:
        return self.submissions.get(user_id)

    def has_submitted(self, user_id: str) -> bool:
        return user_id in self.submissions

    def validate_pick(self, game_id: str, picked_team: str, today_games: List) -> bool:
        for g in today_games:
            if g.game_id == game_id and picked_team in [g.home_team, g.away_team]:
                return True
        return False