import random
import pandas as pd
from datetime import datetime, timedelta

from src.config import BASE_DIR, RANDOM_SEED
random.seed(RANDOM_SEED)

# -----------------------------
# Load Players
# -----------------------------

players = pd.read_csv(
    BASE_DIR / "data" / "users.csv"
)

MATCHES_PER_PLAYER = 10

feedback = []

# -----------------------------
# Compatibility Logic
# -----------------------------

def compatibility_score(player1, player2):

    score = 0

    # Same Game
    if player1["main_game"] == player2["main_game"]:
        score += 35

    # Same Server
    if player1["server"] == player2["server"]:
        score += 20

    # Similar Rank
    ranks = [
        "Bronze",
        "Silver",
        "Gold",
        "Platinum",
        "Diamond",
        "Ascendant",
        "Immortal",
        "Radiant"
    ]

    r1 = ranks.index(player1["rank"])
    r2 = ranks.index(player2["rank"])

    if abs(r1-r2) <= 1:
        score += 20

    # Same Play Time
    if player1["preferred_play_time"] == player2["preferred_play_time"]:
        score += 15

    # Same Communication Style
    if player1["communication_style"] == player2["communication_style"]:
        score += 10

    return score


# -----------------------------
# Generate Feedback
# -----------------------------

for i in range(len(players)):

    current = players.iloc[i]

    chosen = random.sample(
        range(len(players)),
        min(MATCHES_PER_PLAYER, len(players))
    )

    for j in chosen:

        if i == j:
            continue

        other = players.iloc[j]

        score = compatibility_score(
            current,
            other
        )
        probability = min(0.95, score / 100)

        action = 1 if random.random() < probability else 0

        days = random.randint(1, 180)

        feedback.append({

            "player_id": current["player_id"],

            "matched_player_id": other["player_id"],

            "action": action,

            "timestamp": (
                datetime.now()
                - timedelta(days=days)
            ).strftime("%Y-%m-%d")

        })

feedback_df = pd.DataFrame(feedback)

feedback_df.to_csv(
    BASE_DIR / "data" / "feedback.csv",
    index=False
)

print()

print("===============================")

print("feedback.csv generated")

print(f"Total Interactions: {len(feedback_df)}")

print("===============================")