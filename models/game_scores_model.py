from dataclasses import dataclass
from typing import List, Optional

@dataclass
class GameScore:
    game_id: str
    home_team: str
    away_team: str
    home_score: Optional[int]
    away_score: Optional[int]
    status: str
    start_time: Optional[str]

def parse_scores_now(raw_data: dict) -> List[GameScore]:
    games = []
    for game in raw_data.get("games", []):
        home = game.get("homeTeam", {})
        away = game.get("awayTeam", {})

        home_name = home.get("teamAbbrev", "Unknown")
        away_name = away.get("teamAbbrev", "Unknown")

        games.append(GameScore(
            game_id=game.get("id"),
            home_team=home_name,
            away_team=away_name,
            home_score=home.get("score"),
            away_score=away.get("score"),
            status=game.get("gameState"),
            start_time=game.get("startTimeUTC")
        ))
    return games