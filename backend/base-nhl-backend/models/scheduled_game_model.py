from dataclasses import dataclass
from typing import List

@dataclass
class ScheduledGame:
    game_id: str
    home_team: str
    away_team: str
    start_time: str
    status: str

def parse_schedule(raw_data: dict) -> List[ScheduledGame]:
    games = []
    for day in raw_data.get("gameWeek", []):
        for game in day.get("games", []):
            home = game.get("homeTeam", {})
            away = game.get("awayTeam", {})

            home_abbrev = home.get("abbrev", "UNK")
            away_abbrev = away.get("abbrev", "UNK")

            games.append(ScheduledGame(
                game_id=str(game.get("id")),
                home_team=home_abbrev,
                away_team=away_abbrev,
                start_time=game.get("startTimeUTC"),
                status=game.get("gameState")
            ))
    return games