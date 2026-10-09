import os
import joblib
import pandas as pd

from src.config import BASE_DIR


from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix
)

from src.matching_engine import MatchingEngine


class FeedbackLearning:

    # ------------------------------------------
    # Constructor
    # ------------------------------------------

    def __init__(self):

        self.engine = MatchingEngine()

        self.feedback = pd.read_csv(BASE_DIR / "data" / "feedback.csv")

        self.model = LogisticRegression(
            max_iter=1000,
            random_state=42
        )

        self.X = None
        self.y = None

    # ------------------------------------------
    # Build Training Dataset
    # ------------------------------------------

    def build_training_data(self):

        dataset = []

        for _, row in self.feedback.iterrows():

            try:

                scores = self.engine.calculate_scores(

                    row["player_id"],

                    row["matched_player_id"]

                )

                dataset.append({

                    "summary":
                        scores["summary"],

                    "about":
                        scores["about"],

                    "mbti":
                        scores["mbti"],

                    "game":
                        scores["game"],

                    "favorite_games":
                        scores["favorite_games"],

                    "rank":
                        scores["rank"],

                    "server":
                        scores["server"],

                    "playtime":
                        scores["playtime"],

                    "communication":
                        scores["communication"],

                    "playstyle":
                        scores["playstyle"],

                    "accepted":
                        row["action"]

                })

            except Exception as e:
                print(f"Skipping record: {e}")

                continue

        df = pd.DataFrame(dataset)

        self.X = df.drop(
            columns=["accepted"]
        )

        self.y = df["accepted"]

        print()

        print("=" * 60)

        print("Training Dataset Built")

        print(f"Samples : {len(df)}")

        print("=" * 60)
            # ------------------------------------------
    # Train Logistic Regression Model
    # ------------------------------------------

    def train_model(self):

        X_train, X_test, y_train, y_test = train_test_split(

            self.X,

            self.y,

            test_size=0.20,

            random_state=42,

            stratify=self.y

        )

        self.model.fit(

            X_train,

            y_train

        )

        predictions = self.model.predict(

            X_test

        )

        accuracy = accuracy_score(

            y_test,

            predictions

        )

        print()

        print("=" * 60)

        print("MODEL TRAINED SUCCESSFULLY")

        print("=" * 60)

        print(f"Accuracy : {accuracy * 100:.2f}%")

        print()

        print("Confusion Matrix")

        print(

            confusion_matrix(

                y_test,

                predictions

            )

        )

        print()

        print("Classification Report")

        print(

            classification_report(

                y_test,

                predictions

            )

        )

        self.display_feature_importance()

        self.save_model()


    # ------------------------------------------
    # Display Feature Importance
    # ------------------------------------------

    def display_feature_importance(self):

        print()

        print("=" * 60)

        print("LEARNED FEATURE IMPORTANCE")

        print("=" * 60)

        feature_names = list(self.X.columns)

        coefficients = self.model.coef_[0]

        importance = list(

            zip(

                feature_names,

                coefficients

            )

        )

        importance.sort(

            key=lambda x: abs(x[1]),

            reverse=True

        )

        for feature, weight in importance:

            print(

                f"{feature:<20} {weight:.4f}"

            )


    # ------------------------------------------
    # Save Trained Model
    # ------------------------------------------

    def save_model(self):

        os.makedirs(

            BASE_DIR / "models",

            exist_ok=True

        )

        joblib.dump(

            self.model,

            BASE_DIR / "models" / "recommendation_model.pkl"

        )

        print()

        print("=" * 60)

        print("Model Saved Successfully")

        print(BASE_DIR / "models" / "recommendation_model.pkl")

        print("=" * 60)


    # ------------------------------------------
    # Load Trained Model
    # ------------------------------------------

    def load_model(self):

        model_path = BASE_DIR / "models" / "recommendation_model.pkl"

        if not model_path.exists():
            raise FileNotFoundError("Train the model before loading it.")

        self.model = joblib.load(model_path)

        print()

        print("Model Loaded Successfully.")

            # ------------------------------------------
    # Predict Acceptance
    # ------------------------------------------

    def predict_acceptance(self, player_id_1, player_id_2):

        scores = self.engine.calculate_scores(
            player_id_1,
            player_id_2
        )

        sample = pd.DataFrame([{

            "summary": scores["summary"],

            "about": scores["about"],

            "mbti": scores["mbti"],

            "game": scores["game"],

            "favorite_games": scores["favorite_games"],

            "rank": scores["rank"],

            "server": scores["server"],

            "playtime": scores["playtime"],

            "communication": scores["communication"],

            "playstyle": scores["playstyle"]

        }])

        prediction = self.model.predict(sample)[0]

        probability = self.model.predict_proba(sample)[0][1]

        print()

        print("=" * 60)
        print("MATCH PREDICTION")
        print("=" * 60)

        print(f"Player 1 : {player_id_1}")
        print(f"Player 2 : {player_id_2}")

        print()

        if prediction == 1:
            print("Prediction : ACCEPT")
        else:
            print("Prediction : REJECT")

        print(f"Acceptance Probability : {probability * 100:.2f}%")

        print("=" * 60)


# =====================================================
# Main Function
# =====================================================

def main():

    learner = FeedbackLearning()

    learner.build_training_data()

    learner.train_model()

    print()

    print("=" * 60)
    print("Testing Saved Model")
    print("=" * 60)

    learner.load_model()

    while True:

        print()

        print("=" * 60)
        print("Feedback Learning Module")
        print("=" * 60)

        print("1. Predict Match Acceptance")
        print("2. Exit")

        choice = input("\nEnter Choice : ")

        if choice == "1":

            player1 = input(
                "Enter First Player ID : "
            ).upper()

            player2 = input(
                "Enter Second Player ID : "
            ).upper()

            try:

                learner.predict_acceptance(
                    player1,
                    player2
                )

            except Exception as e:

                print(e)

        elif choice == "2":

            print("\nExiting...")

            break

        else:

            print("\nInvalid Choice")


if __name__ == "__main__":

    main()