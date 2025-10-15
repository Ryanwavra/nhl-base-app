from dataclasses import dataclass
from typing import Optional, Dict, Any, List

@dataclass
class GameScore:
    game_id: str
    home_team: str
    away_team: str
    home_score: Optional[int]
    away_score: Optional[int]
    status: str  # e.g. "LIVE", "FINAL", "FUT"
    period: Optional[str] = None
    time_remaining: Optional[str] = None

def parse_scores_now(raw: Dict[str, Any]) -> List[GameScore]:
    games = raw.get("games", [])
    parsed = []

    for g in games:
        parsed.append(GameScore(
            game_id=g.get("id", ""),
            home_team=g.get("home", {}).get("abbrev", "HOME"),
            away_team=g.get("away", {}).get("abbrev", "AWAY"),
            home_score=g.get("home", {}).get("score"),
            away_score=g.get("away", {}).get("score"),
            status=g.get("status", "UNKNOWN"),
            period=g.get("period"),
            time_remaining=g.get("timeRemaining")
        ))

    return parsed