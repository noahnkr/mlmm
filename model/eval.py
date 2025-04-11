import pandas as pd
from sklearn.metrics import accuracy_score, classification_report
from sklearn.preprocessing import StandardScaler
from model.utils import MODELS, load_raw_data
from scraper.utils import REGIONS, ROUNDS

def print_classification_report(X_train, X_test, y_train, y_test):
    scaler = StandardScaler()
    X_train_scl = scaler.fit_transform(X_train)
    X_test_scl = scaler.transform(X_test)

    for name, model in MODELS.items():
        print(f"\nTraining model: {name}")
        
        if name in ["Logistic Regression", "SVM", "KNN"]:
            model.fit(X_train_scl, y_train)
            preds = model.predict(X_test_scl)
        else:
            model.fit(X_train, y_train)
            preds = model.predict(X_test)
        
        print(classification_report(y_test, preds))

def print_correct_upsets(preds, y_test, info_test):
    for pred, true, info in zip(preds, y_test, info_test):
        if pred != true:
            continue

        # Determine predicted winner and their seed
        predicted_winner = info["team_a"] if pred == 1 else info["team_b"]
        predicted_seed = info["team_a_seed"] if pred == 1 else info["team_b_seed"]
        opponent_seed = info["team_b_seed"] if pred == 1 else info["team_a_seed"]

        # If predicted winner is a higher seed (lower ranked team wins)
        if predicted_seed > opponent_seed:
            print(f"{info["year"]} {info["round"]} {info["region"]}")
            print(f"{info["team_a"]} ({info["team_a_seed"]}) vs {info["team_b"]} ({info["team_b_seed"]})")
            print(f"Predicted: {predicted_winner} | Correct: {info["winner"]}")
            print("---")

def simulate_tournament(year, model):
    matchups, team_stats = load_raw_data()

    current_games = matchups[(matchups["year"] == year) & (matchups["round"] == "First")]
    current_games.sort_values(by=["region", "team_a_seed", "team_b_seed"])

def _simulate_tournament_round():
    pass