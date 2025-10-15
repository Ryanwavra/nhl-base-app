import os
import requests
from dotenv import load_dotenv
from typing import Dict, Any
from datetime import date, timedelta, datetime
from zoneinfo import ZoneInfo
import tzlocal

from models.scheduled_game_model import ScheduledGame, parse_schedule
from models.live_scores_model import GameScore, parse_scores_now

load_dotenv()


class NHLApiClient:
    def __init__(self):
        self.base_url = os.getenv("NHL_API_BASE_URL")
        if not self.base_url:
            raise ValueError("NHL_API_BASE_URL not set in .env")

    def get_schedule_by_date(self, date: str) -> Dict[str, Any]:
        """Fetch scheduled games for a specific date (YYYY-MM-DD)."""
        url = f"{self.base_url}/schedule/{date}"
        try:
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"Error fetching schedule for {date}: {e}")
            return {}

    def get_live_scores(self) -> Dict[str, Any]:
        """Fetch live scores and game status for today."""
        url = f"{self.base_url}/scoreboard/now"
        try:
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"Error fetching live scores: {e}")
            return {}

    def get_parsed_schedule(self, iso_date: str) -> list[ScheduledGame]:
        raw = self.get_schedule_by_date(iso_date)
        return parse_schedule(raw)

    def get_today_games(self) -> list[ScheduledGame]:
        today = date.today().isoformat()
        raw = self.get_schedule_by_date(today)
        all_games = parse_schedule(raw)
        return [g for g in all_games if g.start_time and g.start_time[:10] == today]

    def get_tomorrow_games(self) -> list[ScheduledGame]:
        tomorrow = (date.today() + timedelta(days=1)).isoformat()
        raw = self.get_schedule_by_date(tomorrow)
        all_games = parse_schedule(raw)
        return [g for g in all_games if g.start_time and g.start_time[:10] == tomorrow]

    def get_parsed_scores(self) -> list[GameScore]:
        raw = self.get_live_scores()
        return parse_scores_now(raw)

    def convert_utc_to_local(self, utc_str: str) -> str:
        try:
            local_tz = tzlocal.get_localzone()
            utc_dt = datetime.fromisoformat(utc_str.replace("Z", "+00:00"))
            local_dt = utc_dt.astimezone(local_tz)
            return local_dt.strftime("%Y-%m-%d %I:%M %p %Z")
        except Exception as e:
            print(f"Error converting time: {e}")
            return utc_str


