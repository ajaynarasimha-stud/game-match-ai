"""
Global configuration for GameMatch AI
"""
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent


# -------------------------
# Dataset Settings
# -------------------------

NUMBER_OF_PLAYERS = 150

# -------------------------
# Recommendation Weights
# -------------------------

TEXT_WEIGHT = 0.25
ABOUT_WEIGHT = 0.15
MBTI_WEIGHT = 0.10
GAME_WEIGHT = 0.10
RANK_WEIGHT = 0.10
SERVER_WEIGHT = 0.05
PLAYTIME_WEIGHT = 0.05

FAVORITE_GAMES_WEIGHT = 0.10
COMMUNICATION_WEIGHT = 0.05
PLAYSTYLE_WEIGHT = 0.05

# -------------------------
# Random Seed
# -------------------------

RANDOM_SEED = 42