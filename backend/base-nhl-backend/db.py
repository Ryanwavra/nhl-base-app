import os
from dotenv import load_dotenv
from supabase import create_client

load_dotenv()

# Load credentials from environment variables
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")

# Initialize the Supabase client
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# -----------------------------
# Submissions
# -----------------------------
def create_submission(user_id: str, tiebreaker_guess: int) -> int:
    """Insert a new submission and return its ID."""
    response = supabase.table("submissions").insert({
        "user_id": user_id,
        "tiebreaker_guess": tiebreaker_guess
    }).execute()

    if response.data:
        return response.data[0]["id"]
    else:
        raise Exception(f"Failed to create submission: {response}")

# -----------------------------
# Picks
# -----------------------------
def add_pick(submission_id: int, game_id: str, picked_team: str):
    """Insert a pick tied to a submission."""
    response = supabase.table("picks").insert({
        "submission_id": submission_id,
        "game_id": game_id,
        "picked_team": picked_team
    }).execute()
    return response.data

def get_picks_for_submission(submission_id: int):
    """Fetch all picks for a given submission."""
    response = supabase.table("picks").select("*").eq("submission_id", submission_id).execute()
    return response.data

# -----------------------------
# Utility Queries
# -----------------------------
def get_submissions():
    """Fetch all submissions."""
    response = supabase.table("submissions").select("*").execute()
    return response.data

if __name__ == "__main__":
    # 1. Insert a submission
    submission_resp = supabase.table("submissions").insert({
        "user_id": "debug-user",
        "tiebreaker_guess": 42
    }).execute()
    print("Submission insert response:", submission_resp)

    # Grab the new submission_id
    sid = submission_resp.data[0]["id"]

    # 2. Insert a couple of picks tied to that submission
    pick1 = supabase.table("picks").insert({
        "submission_id": sid,
        "game_id": "20251015-OTT-BUF",
        "picked_team": "OTT"
    }).execute()
    print("Pick 1 insert response:", pick1)

    pick2 = supabase.table("picks").insert({
        "submission_id": sid,
        "game_id": "20251015-FLA-DET",
        "picked_team": "DET"
    }).execute()
    print("Pick 2 insert response:", pick2)

    # 3. Fetch back all picks for this submission
    picks_resp = supabase.table("picks").select("*").eq("submission_id", sid).execute()
    print("Picks fetched for submission:", picks_resp)