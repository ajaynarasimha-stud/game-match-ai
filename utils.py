# --------------------------
# Rank Compatibility
# --------------------------

rank_order = {

    "Bronze":1,

    "Silver":2,

    "Gold":3,

    "Platinum":4,

    "Diamond":5,

    "Ascendant":6,

    "Immortal":7,

    "Radiant":8

}

def rank_score(rank1,rank2):

    diff = abs(
        rank_order[rank1]
        -
        rank_order[rank2]
    )

    if diff==0:
        return 100

    elif diff==1:
        return 90

    elif diff==2:
        return 75

    elif diff==3:
        return 60

    return 40

# --------------------------
# Server Score
# --------------------------

def server_score(server1,server2):

    if server1==server2:
        return 100

    return 50

# --------------------------
# Game Score
# --------------------------

def game_score(game1,game2):

    if game1==game2:
        return 100

    return 40

# --------------------------
# Play Time Score
# --------------------------

def playtime_score(time1,time2):

    if time1==time2:
        return 100

    return 60

# --------------------------
# MBTI Score
# --------------------------

def mbti_score(mbti1, mbti2):

    score = 0

    # Same Introvert / Extrovert
    if mbti1[0] == mbti2[0]:
        score += 25

    # Same Sensing / Intuition
    if mbti1[1] == mbti2[1]:
        score += 25

    # Same Thinking / Feeling
    if mbti1[2] == mbti2[2]:
        score += 25

    # Same Judging / Perceiving
    if mbti1[3] == mbti2[3]:
        score += 25

    return score


def favorite_games_score(games1, games2):

    list1 = [game.strip() for game in games1.split(",")]
    list2 = [game.strip() for game in games2.split(",")]

    common = len(
        set(list1).intersection(set(list2))
    )

    if common == 3:
        return 100

    elif common == 2:
        return 85

    elif common == 1:
        return 70

    return 40


# --------------------------
# Communication Score
# --------------------------

def communication_score(style1, style2):

    if style1 == style2:
        return 100

    if (
        style1 == "Balanced"
        or
        style2 == "Balanced"
    ):
        return 80

    return 60


# --------------------------
# Play Style Score
# --------------------------

def playstyle_score(style1, style2):

    if style1 == style2:
        return 100

    return 70


# --------------------------
# Compatibility Label
# --------------------------

def compatibility_label(score):

    if score >= 90:
        return "Excellent Match"

    elif score >= 80:
        return "Very Good Match"

    elif score >= 70:
        return "Good Match"

    elif score >= 60:
        return "Average Match"

    return "Low Compatibility"

# --------------------------
# Recommendation Explanation
# --------------------------

def explain_recommendation(player1, player2):

    reasons = []

    if player1["main_game"] == player2["main_game"]:
        reasons.append("Same Main Game")

    #if player1["favorite_games"] == player2["favorite_games"]:
    #    reasons.append("Similar Favorite Games")

    games1 = {
        game.strip()
        for game in player1["favorite_games"].split(",")
    }

    games2 = {
        game.strip()
        for game in player2["favorite_games"].split(",")
    }

    if len(games1.intersection(games2)) >= 2:
        reasons.append("Similar Favorite Games")

    if player1["server"] == player2["server"]:
        reasons.append("Same Server")

    if rank_score(player1["rank"], player2["rank"]) >= 90:
        reasons.append("Similar Skill Rank")

    if player1["preferred_role"] == player2["preferred_role"]:
        reasons.append("Same Preferred Role")

    if player1["preferred_play_time"] == player2["preferred_play_time"]:
        reasons.append("Same Preferred Play Time")

    if player1["communication_style"] == player2["communication_style"]:
        reasons.append("Similar Communication Style")

    if player1["play_style"] == player2["play_style"]:
        reasons.append("Similar Play Style")

    if player1["mbti"] == player2["mbti"]:
        reasons.append("Compatible Personality")

    if len(reasons) == 0:
        reasons.append("Overall profile similarity")

    return reasons