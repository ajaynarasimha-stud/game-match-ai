"""
performance_analysis.py

Generate performance graphs for GameMatch AI.
"""

import os
import joblib
import pandas as pd
import matplotlib.pyplot as plt
from src.config import BASE_DIR

from sklearn.metrics import (
    confusion_matrix,
    ConfusionMatrixDisplay,
    accuracy_score
)

from sklearn.model_selection import train_test_split

from src.feedback_learning import FeedbackLearning



class PerformanceAnalysis:

    def __init__(self):

        self.learner = FeedbackLearning()

        self.learner.build_training_data()

        self.X = self.learner.X
        self.y = self.learner.y

        model_path = BASE_DIR / "models" / "recommendation_model.pkl"

        if model_path.exists():

            self.model = joblib.load(model_path)

            print("Loaded existing trained model.")

        else:

            print("No trained model found.")
            print("Training a new model...")

            self.learner.train_model()

            self.model = self.learner.model

        os.makedirs(BASE_DIR / "graphs", exist_ok=True)

    # ----------------------------------------------------
    # Split Dataset
    # ----------------------------------------------------

    def split_data(self):

        return train_test_split(

            self.X,

            self.y,

            test_size=0.20,

            random_state=42,

            stratify=self.y

        )

    # ----------------------------------------------------
    # Accuracy Graph
    # ----------------------------------------------------

    def accuracy_graph(self):

        X_train, X_test, y_train, y_test = self.split_data()

        predictions = self.model.predict(X_test)

        accuracy = accuracy_score(

            y_test,

            predictions

        )

        plt.figure(figsize=(6,5))

        plt.bar(

            ["Accuracy"],

            [accuracy * 100]

        )

        plt.ylim(0,100)

        plt.ylabel("Percentage")

        plt.title("Recommendation Model Accuracy")

        plt.savefig(

            BASE_DIR / "graphs" / "accuracy.png",

            dpi=300,

            bbox_inches="tight"

        )

        plt.close()

        print("accuracy.png generated")
    # ----------------------------------------------------
    # Confusion Matrix Graph
    # ----------------------------------------------------

    def confusion_matrix_graph(self):

        X_train, X_test, y_train, y_test = self.split_data()

        predictions = self.model.predict(X_test)

        cm = confusion_matrix(
            y_test,
            predictions
        )

        plt.figure(figsize=(6,6))

        disp = ConfusionMatrixDisplay(
            confusion_matrix=cm
        )

        disp.plot()

        plt.title("Confusion Matrix")

        plt.savefig(
            BASE_DIR / "graphs" / "confusion_matrix.png",
            dpi=300,
            bbox_inches="tight"
        )

        plt.close()

        print("confusion_matrix.png generated")


    # ----------------------------------------------------
    # Feature Importance Graph
    # ----------------------------------------------------

    def feature_importance_graph(self):

        feature_names = list(self.X.columns)

        coefficients = self.model.coef_[0]

        plt.figure(figsize=(10,6))

        plt.bar(
            feature_names,
            coefficients
        )

        plt.xticks(rotation=45)

        plt.ylabel("Coefficient")

        plt.title("Feature Importance")

        plt.tight_layout()

        plt.savefig(
            BASE_DIR / "graphs" / "feature_importance.png",
            dpi=300,
            bbox_inches="tight"
        )

        plt.close()

        print("feature_importance.png generated")


    # ----------------------------------------------------
    # Rank Distribution
    # ----------------------------------------------------

    def rank_distribution(self):

        users = pd.read_csv(
            BASE_DIR / "data" / "users.csv"
        )

        plt.figure(figsize=(8,5))

        users["rank"].value_counts().sort_index().plot(
            kind="bar"
        )

        plt.title("Player Rank Distribution")

        plt.xlabel("Rank")

        plt.ylabel("Number of Players")

        plt.tight_layout()

        plt.savefig(
            BASE_DIR / "graphs" / "rank_distribution.png",
            dpi=300,
            bbox_inches="tight"
        )

        plt.close()

        print("rank_distribution.png generated")

            # ----------------------------------------------------
    # Game Distribution
    # ----------------------------------------------------

    def game_distribution(self):

        users = pd.read_csv(
            BASE_DIR / "data" / "users.csv"
        )

        plt.figure(figsize=(9,5))

        users["main_game"].value_counts().plot(
            kind="bar"
        )

        plt.title("Main Game Distribution")

        plt.xlabel("Game")

        plt.ylabel("Players")

        plt.xticks(rotation=30)

        plt.tight_layout()

        plt.savefig(
            BASE_DIR / "graphs" / "game_distribution.png",
            dpi=300,
            bbox_inches="tight"
        )

        plt.close()

        print("game_distribution.png generated")


    # ----------------------------------------------------
    # Feedback Distribution
    # ----------------------------------------------------

    def feedback_distribution(self):

        feedback = pd.read_csv(
            BASE_DIR / "data" / "feedback.csv"
        )

        plt.figure(figsize=(5,5))

        feedback["action"].value_counts().sort_index().plot(
            kind="pie",
            autopct="%1.1f%%",
            labels=["Rejected", "Accepted"]
        )

        plt.ylabel("")

        plt.title("Feedback Distribution")

        plt.tight_layout()

        plt.savefig(
            BASE_DIR / "graphs" / "feedback_distribution.png",
            dpi=300,
            bbox_inches="tight"
        )

        plt.close()

        print("feedback_distribution.png generated")


    # ----------------------------------------------------
    # Generate All Graphs
    # ----------------------------------------------------

    def generate_all_graphs(self):

        print("\nGenerating Graphs...\n")

        self.accuracy_graph()

        self.confusion_matrix_graph()

        self.feature_importance_graph()

        self.rank_distribution()

        self.game_distribution()

        self.feedback_distribution()

        print("\nAll graphs generated successfully!")



# ======================================================
# Main
# ======================================================

def main():

    analysis = PerformanceAnalysis()

    analysis.generate_all_graphs()


if __name__ == "__main__":

    main()