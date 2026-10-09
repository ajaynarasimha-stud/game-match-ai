import random
import pandas as pd
from faker import Faker

from src.config import (
    BASE_DIR,
    NUMBER_OF_PLAYERS,
    RANDOM_SEED
)

fake = Faker()

random.seed(RANDOM_SEED)
Faker.seed(RANDOM_SEED)

# ----------------------------
# Data Lists
# ----------------------------

servers = [
    "Asia",
    "Europe",
    "North America",
    "South America",
    "Middle East"
]

games = [
    "Valorant",
    "Counter-Strike 2",
    "Apex Legends",
    "Rainbow Six Siege",
    "Marvel Rivals",
    "Overwatch 2",
    "League of Legends",
    "Dota 2"
]

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

roles = [
    "Duelist",
    "Controller",
    "Initiator",
    "Sentinel",
    "Tank",
    "Support",
    "DPS",
    "Flex"
]

communication = [
    "Very Talkative",
    "Talkative",
    "Balanced",
    "Quiet"
]

play_styles = [
    "Aggressive",
    "Strategic",
    "Supportive",
    "Flexible",
    "Objective Focused"
]

gaming_goals = [
    "Rank Push",
    "Competitive",
    "Casual Fun",
    "Tournament Practice",
    "Finding Long-term Squad"
]

play_times = [
    "Morning",
    "Afternoon",
    "Evening",
    "Late Night"
]

mbti_types = [
    "INTJ","INTP","ENTJ","ENTP",
    "INFJ","INFP","ENFJ","ENFP",
    "ISTJ","ISFJ","ESTJ","ESFJ",
    "ISTP","ISFP","ESTP","ESFP"
]

interests = [
    "FPS",
    "MOBA",
    "Strategy",
    "Esports",
    "Streaming",
    "Anime",
    "Technology",
    "RPG",
    "Open World",
    "Indie Games"
]

#summary_templates = [
#    "Competitive {} player with excellent teamwork and communication skills. Focused on improving mechanics and climbing ranked ladders.",
#    "Experienced {} player who enjoys coordinated team play and tactical decision making.",
#    "Dedicated {} enthusiast looking for reliable teammates for competitive matches.",
#    "Passionate {} gamer who values strategy, communication and continuous improvement.",
#    "Versatile {} player comfortable adapting to different situations and teammates."
#]

#gaming_summary = (
#    f"{random.choice(['Competitive', 'Experienced', 'Dedicated', 'Passionate'])} "
#    f"{main_game} player specializing in {profile['preferred_role']} gameplay. "
#    f"Enjoys {profile['gaming_goal'].lower()} with {profile['communication_style'].lower()} communication. "
#    f"Usually plays during the {profile['preferred_play_time'].lower()}."
#)

#about_templates = [
#    "I enjoy learning from every match and helping teammates improve.",
#    "Calm player who believes communication wins games.",
#    "I like making new gaming friends and playing consistently.",
#    "Positive mindset with focus on teamwork and sportsmanship.",
#    "I enjoy competitive matches but always keep the atmosphere fun."
#]

# ----------------------------
# Generate Dataset
# ----------------------------

players = []

for i in range(1, NUMBER_OF_PLAYERS + 1):

    main_game = random.choice(games)
    server = random.choice(servers)
    rank = random.choice(ranks)
    preferred_role = random.choice(roles)
    communication_style = random.choice(communication)
    play_style = random.choice(play_styles)
    gaming_goal = random.choice(gaming_goals)
    preferred_play_time = random.choice(play_times)
    mbti = random.choice(mbti_types)

    gaming_summary = (
    f"{random.choice(['Competitive', 'Experienced', 'Dedicated', 'Passionate'])} "
    f"{main_game} player specializing in {preferred_role} gameplay. "
    f"Enjoys {gaming_goal.lower()} with {communication_style.lower()} communication. "
    f"Usually plays during the {preferred_play_time.lower()}."
    )

    about_me = (
        f"I enjoy {random.choice(['teamwork', 'competitive matches', 'learning new strategies'])}. "
        f"My favorite genres are {random.choice(interests)} and {random.choice(interests)}. "
        f"I am looking for teammates who enjoy {gaming_goal.lower()}."
    )

    favorite_games = [main_game]

    remaining = [g for g in games if g != main_game]

    favorite_games.extend(
        random.sample(remaining, 2)
    )

    random.shuffle(favorite_games)

    profile = {

        "player_id": f"G{i:03}",

        "gamer_tag": fake.user_name(),

        "age": random.randint(18, 35),

        "server": server,

        "main_game": main_game,

        "favorite_games": ", ".join(favorite_games),

        "rank": rank,

        "preferred_role": preferred_role,

        "communication_style": communication_style,

        "play_style": play_style,

        "gaming_goal": gaming_goal,

        "gaming_summary": gaming_summary,

        "about_me": about_me,

        "mbti": mbti,

        "preferred_play_time": preferred_play_time,

        "interests":
            ", ".join(random.sample(interests, 3))

    }

    players.append(profile)

df = pd.DataFrame(players)

df.to_csv(
    BASE_DIR / "data" / "users.csv",
    index=False
)

print()

print("======================================")

print(" users.csv generated successfully!")

print(" Total Players :", len(df))

print("======================================")