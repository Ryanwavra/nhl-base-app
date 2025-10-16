from dataclasses import dataclass
from typing import Optional, List, Dict, Any
from datetime import datetime, timedelta
import pytz

@dataclass
class LiveScore:
    game_id: str
    home_team: str
    away_team: str
    home_score: Optional[int]
    away_score: Optional[int]
    status: str  # "LIVE", "Done", or "FUT"
    period: Optional[int] = None
    time_remaining: Optional[str] = None
    game_date: Optional[str] = None  # Format: "YYYY-MM-DD"

def parse_live_scores(raw: Dict[str, Any]) -> List[LiveScore]:
    scores = []

    for day in raw.get("gamesByDate", []):
        for g in day.get("games", []):
            home = g.get("homeTeam", {})
            away = g.get("awayTeam", {})
            status = g.get("gameState", "UNKNOWN")

            # Convert "OFF" to "Done" if scores are present
            if status == "OFF" and home.get("score") is not None and away.get("score") is not None:
                status = "Done"

            scores.append(LiveScore(
                home_team=home.get("abbrev", "HOME"),
                away_team=away.get("abbrev", "AWAY"),
                home_score=home.get("score"),
                away_score=away.get("score"),
                status=status,
                period=g.get("period"),
                time_remaining=None,
                game_date=g.get("gameDate")
            ))

    return scores

def should_show_game(game: LiveScore) -> bool:
    now = datetime.now(pytz.timezone("US/Eastern"))

    if game.status == "LIVE":
        return True

    if game.status == "Done" and game.game_date:
        try:
            game_day = datetime.strptime(game.game_date, "%Y-%m-%d").date()
            cutoff = datetime.combine(game_day + timedelta(days=1), datetime.min.time(), tzinfo=now.tzinfo) + timedelta(hours=4)
            return now < cutoff
        except ValueError:
            return False

    return False