import json
from typing import List, Dict, Optional
from pathlib import Path

class MockAPIClient:
    def __init__(self, fixtures_dir: str = "tests/fixtures"):
        self.fixtures_dir = Path(fixtures_dir)

    def _load_fixture(self, filename: str):
        filepath = self.fixtures_dir / filename
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)

    def get_upcoming_games(self, date: Optional[str] = None) -> List[Dict]:
        return self._load_fixture("upcoming_games.json")

    def get_completed_games(self, date: Optional[str] = None) -> List[Dict]:
        return self._load_fixture("completed_games.json")
