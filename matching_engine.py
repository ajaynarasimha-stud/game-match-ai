import pandas as pd
from src.config import BASE_DIR


from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from src.config import (
    BASE_DIR,
    TEXT_WEIGHT,
    ABOUT_WEIGHT,
    MBTI_WEIGHT,
    GAME_WEIGHT,
    FAVORITE_GAMES_WEIGHT,
    RANK_WEIGHT,
    SERVER_WEIGHT,
    PLAYTIME_WEIGHT,
    COMMUNICATION_WEIGHT,
    PLAYSTYLE_WEIGHT
)

from src.utils import (
    mbti_score,
    rank_score,
    server_score,
    game_score,
    playtime_score,
    favorite_games_score,
    communication_score,
    playstyle_score,
    compatibility_label,
    explain_recommendation
)


class MatchingEngine:

    # --------------------------------------------------
    # Constructor
    # --------------------------------------------------

    def __init__(self):

        self.players = pd.read_csv(BASE_DIR / "data" / "users.csv")

        self.summary_vectorizer = None
        self.about_vectorizer = None

        self.summary_similarity = None
        self.about_similarity = None

        self.prepare_nlp()


    # --------------------------------------------------
    # Prepare TF-IDF
    # --------------------------------------------------

    def prepare_nlp(self):

        self.players["summary_text"] = (
            self.players["gaming_summary"]
            .fillna("")
            .astype(str)
        )

        self.players["about_text"] = (
            self.players["about_me"]
            .fillna("")
            .astype(str)
        )

        self.summary_vectorizer = TfidfVectorizer(
            stop_words="english"
        )

        summary_matrix = self.summary_vectorizer.fit_transform(
            self.players["summary_text"]
        )

        self.summary_similarity = cosine_similarity(
            summary_matrix
        )

        self.about_vectorizer = TfidfVectorizer(
            stop_words="english"
        )

        about_matrix = self.about_vectorizer.fit_transform(
            self.players["about_text"]
        )

        self.about_similarity = cosine_similarity(
            about_matrix
        )


    # --------------------------------------------------
    # Get Player Index
    # --------------------------------------------------

    def get_index(self, player_id):

        result = self.players.index[
            self.players["player_id"] == player_id
        ]

        if len(result) == 0:

            raise ValueError(
                f"Player '{player_id}' not found."
            )

        return result[0]


    # --------------------------------------------------
    # Get Player
    # --------------------------------------------------

    def get_player(self, player_id):

        index = self.get_index(player_id)

        return self.players.iloc[index]


    # --------------------------------------------------
    # Summary Similarity
    # --------------------------------------------------

    def summary_score(self, index1, index2):

        return (
            self.summary_similarity[index1][index2]
            * 100
        )


    # --------------------------------------------------
    # About Similarity
    # --------------------------------------------------

    def about_score(self, index1, index2):

        return (
            self.about_similarity[index1][index2]
            * 100
        )


    # --------------------------------------------------
    # Feature Scores
    # --------------------------------------------------

    def calculate_scores(self, player_id_1, player_id_2):

        player1 = self.get_player(player_id_1)

        player2 = self.get_player(player_id_2)

        idx1 = self.get_index(player_id_1)

        idx2 = self.get_index(player_id_2)

        scores = {

            "summary":

                self.summary_score(
                    idx1,
                    idx2
                ),

            "about":

                self.about_score(
                    idx1,
                    idx2
                ),

            "mbti":

                mbti_score(
                    player1["mbti"],
                    player2["mbti"]
                ),

            "game":

                game_score(
                    player1["main_game"],
                    player2["main_game"]
                ),

            "favorite_games":

                favorite_games_score(
                    player1["favorite_games"],
                    player2["favorite_games"]
                ),

            "rank":

                rank_score(
                    player1["rank"],
                    player2["rank"]
                ),

            "server":

                server_score(
                    player1["server"],
                    player2["server"]
                ),

            "playtime":

                playtime_score(
                    player1["preferred_play_time"],
                    player2["preferred_play_time"]
                ),

            "communication":

                communication_score(
                    player1["communication_style"],
                    player2["communication_style"]
                ),

            "playstyle":

                playstyle_score(
                    player1["play_style"],
                    player2["play_style"]
                )

        }

        return scores
        # --------------------------------------------------
    # Final Compatibility Score
    # --------------------------------------------------

    def calculate_compatibility(self, player_id_1, player_id_2):

        scores = self.calculate_scores(
            player_id_1,
            player_id_2
        )

        player1 = self.get_player(player_id_1)
        player2 = self.get_player(player_id_2)

        final_score = (

            scores["summary"] * TEXT_WEIGHT +

            scores["about"] * ABOUT_WEIGHT +

            scores["mbti"] * MBTI_WEIGHT +

            scores["game"] * GAME_WEIGHT +

            scores["rank"] * RANK_WEIGHT +

            scores["favorite_games"] * FAVORITE_GAMES_WEIGHT +

            scores["server"] * SERVER_WEIGHT +

            scores["playtime"] * PLAYTIME_WEIGHT +

            scores["communication"] * COMMUNICATION_WEIGHT +

            scores["playstyle"] * PLAYSTYLE_WEIGHT

        )

        final_score = round(final_score, 2)

        match = {

            "player_id": player2["player_id"],

            "gamer_tag": player2["gamer_tag"],

            "main_game": player2["main_game"],

            "favorite_games": player2["favorite_games"],

            "rank": player2["rank"],

            "preferred_role": player2["preferred_role"],

            "server": player2["server"],

            "communication_style":
                player2["communication_style"],

            "play_style":
                player2["play_style"],

            "gaming_goal":
                player2["gaming_goal"],

            "preferred_play_time":
                player2["preferred_play_time"],

            "mbti":
                player2["mbti"],

            "compatibility_score":
                final_score,

            "compatibility_level":
                compatibility_label(
                    final_score
                ),

            "reasons":
                explain_recommendation(
                    player1,
                    player2
                )

        }

        return match


    # --------------------------------------------------
    # Recommend Players
    # --------------------------------------------------

    def recommend_players(
        self,
        player_id,
        top_n=5
    ):

        recommendations = []

        for _, row in self.players.iterrows():

            other_id = row["player_id"]

            if other_id == player_id:
                continue

            recommendation = self.calculate_compatibility(

                player_id,

                other_id

            )

            recommendations.append(
                recommendation
            )

        recommendations.sort(

            key=lambda x:
            x["compatibility_score"],

            reverse=True

        )

        return recommendations[:top_n]


    # --------------------------------------------------
    # Get Best Match
    # --------------------------------------------------

    def get_best_match(self, player_id):

        matches = self.recommend_players(

            player_id,

            1

        )

        return matches[0]


    # --------------------------------------------------
    # Get Top Matches
    # --------------------------------------------------

    def get_top_matches(

        self,

        player_id,

        number_of_matches=5

    ):

        return self.recommend_players(

            player_id,

            number_of_matches

        )


    # --------------------------------------------------
    # Compare Two Players
    # --------------------------------------------------

    def compare_players(

        self,

        player_id_1,

        player_id_2

    ):

        scores = self.calculate_scores(

            player_id_1,

            player_id_2

        )

        compatibility = self.calculate_compatibility(

            player_id_1,

            player_id_2

        )

        return {

            "player1":
                self.get_player(player_id_1),

            "player2":
                self.get_player(player_id_2),

            "scores":
                scores,

            "result":
                compatibility

        }
        # --------------------------------------------------
    # Display Player Profile
    # --------------------------------------------------

    def show_player(self, player_id):

        player = self.get_player(player_id)

        print("\n" + "=" * 60)
        print("PLAYER PROFILE")
        print("=" * 60)

        print(f"Player ID            : {player['player_id']}")
        print(f"Gamer Tag            : {player['gamer_tag']}")
        print(f"Age                  : {player['age']}")
        print(f"Server               : {player['server']}")
        print(f"Main Game            : {player['main_game']}")
        print(f"Favorite Games       : {player['favorite_games']}")
        print(f"Rank                 : {player['rank']}")
        print(f"Preferred Role       : {player['preferred_role']}")
        print(f"Communication Style  : {player['communication_style']}")
        print(f"Play Style           : {player['play_style']}")
        print(f"Gaming Goal          : {player['gaming_goal']}")
        print(f"Preferred Play Time  : {player['preferred_play_time']}")
        print(f"MBTI                : {player['mbti']}")
        print(f"Gaming Summary      : {player['gaming_summary']}")
        print(f"About Me            : {player['about_me']}")

        print("=" * 60)

    # --------------------------------------------------
    # Display Match
    # --------------------------------------------------

    def show_match(self, match):

        print("\n" + "=" * 60)

        print(f"Gamer Tag : {match['gamer_tag']}")
        print(f"Player ID : {match['player_id']}")
        print(f"Game      : {match['main_game']}")
        print(f"Rank      : {match['rank']}")
        print(f"Role      : {match['preferred_role']}")
        print(f"Server    : {match['server']}")
        print(f"MBTI      : {match['mbti']}")

        print()

        print(
            f"Compatibility : {match['compatibility_score']}%"
        )

        print(
            f"Level : {match['compatibility_level']}"
        )

        print()

        print("Why Recommended?")

        for reason in match["reasons"]:

            print(f"✓ {reason}")

        print("=" * 60)

    # --------------------------------------------------
    # Display Top Matches
    # --------------------------------------------------

    def show_top_matches(self, player_id, top_n=5):

        matches = self.get_top_matches(
            player_id,
            top_n
        )

        print("\n")
        print("=" * 70)
        print(f"TOP {top_n} RECOMMENDED TEAMMATES")
        print("=" * 70)

        for i, match in enumerate(matches, start=1):

            print(f"\nRecommendation #{i}")

            self.show_match(match)

        return matches

    # --------------------------------------------------
    # Compatibility Report
    # --------------------------------------------------

    def compatibility_report(self, player1, player2):

        report = self.compare_players(
            player1,
            player2
        )

        scores = report["scores"]

        result = report["result"]

        print("\n")
        print("=" * 70)
        print("COMPATIBILITY REPORT")
        print("=" * 70)

        print(f"Player 1 : {player1}")
        print(f"Player 2 : {player2}")

        print("\nFeature Scores")

        print(f"Gaming Summary     : {scores['summary']:.2f}")
        print(f"About Me           : {scores['about']:.2f}")
        print(f"MBTI              : {scores['mbti']}")
        print(f"Main Game         : {scores['game']}")
        print(f"Favorite Games    : {scores['favorite_games']}")
        print(f"Rank              : {scores['rank']}")
        print(f"Server            : {scores['server']}")
        print(f"Play Time         : {scores['playtime']}")
        print(f"Communication     : {scores['communication']}")
        print(f"Play Style        : {scores['playstyle']}")

        print("\nOverall Score")

        print(
            f"{result['compatibility_score']}%"
        )

        print(
            result["compatibility_level"]
        )

        print("\nRecommendation Reasons")

        for reason in result["reasons"]:

            print(f"✓ {reason}")

        print("=" * 70)


# ======================================================
# Main Program
# ======================================================

def main():

    engine = MatchingEngine()

    while True:

        print("\n")
        print("=" * 60)
        print("GameMatch AI")
        print("=" * 60)

        print("1. View Player Profile")
        print("2. Get Top 5 Teammates")
        print("3. Compare Two Players")
        print("4. Exit")

        choice = input("\nEnter Choice : ")

        if choice == "1":

            player_id = input(
                "Enter Player ID : "
            ).upper()

            try:

                engine.show_player(
                    player_id
                )

            except Exception as e:

                print(e)

        elif choice == "2":

            player_id = input(
                "Enter Player ID : "
            ).upper()

            try:

                engine.show_top_matches(
                    player_id,
                    5
                )

            except Exception as e:

                print(e)

        elif choice == "3":

            player1 = input(
                "Enter First Player ID : "
            ).upper()

            player2 = input(
                "Enter Second Player ID : "
            ).upper()

            try:

                engine.compatibility_report(
                    player1,
                    player2
                )

            except Exception as e:

                print(e)

        elif choice == "4":

            print("\nThank you for using GameMatch AI.")

            break

        else:

            print("\nInvalid Choice.")


if __name__ == "__main__":

    main()
