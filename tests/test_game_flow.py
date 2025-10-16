import json
from models.user_pick_model import UserPick, PickManager

def load_test_data(filepath: str):
    with open(filepath, "r") as f:
        return json.load(f)

def test_submission():
    data = load_test_data("test_submission.json")

    # Convert picks to UserPick objects
    picks = [UserPick(**p) for p in data["picks"]]

    # Instantiate PickManager
    manager = PickManager()

    # Submit picks
    success = manager.submit_picks(
        user_id=data["user_id"],
        picks=picks,
        tiebreaker_guess=data["tiebreaker_guess"]
    )

    # Output results
    if success:
        submission = manager.get_submission(data["user_id"])
        print("✅ Submission stored successfully:")
        print(submission)
    else:
        print("❌ Submission failed validation.")

if __name__ == "__main__":
    test_submission()