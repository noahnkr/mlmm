import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB

MODELS = {
    "Logistic Regression": LogisticRegression(max_iter=1000),
    "SVM": SVC(kernel="linear"),
    "Random Forest": RandomForestClassifier(n_estimators=100),
    "KNN": KNeighborsClassifier(),
    "Naive Bayes": GaussianNB()
}

def get_team_vector(year, team, seed, team_stats):
    row = team_stats[(team_stats["year"] == year) & (team_stats["team"] == team)].copy()
    if row.empty:
        return None
    row["seed"] = seed
    return row.drop(columns=["year", "team"]).values.flatten() # Remove redundant features, convert to np array

def load_dataset():
    X, y, info = [], [], []

    matchups = pd.read_csv("data/matchups.csv")
    team_stats = pd.read_csv("data/stats.csv")

    for _, row in matchups.iterrows():
        v_a = get_team_vector(row["year"], row["team_a"], row["team_a_seed"], team_stats)
        v_b = get_team_vector(row["year"], row["team_b"], row["team_b_seed"], team_stats)

        if v_a is None or v_b is None:
            continue
        
        dv = v_a - v_b # Feature vector is the difference in both team's stats and seeding
        X.append(dv)
        y.append(1 if row["winner"] == row["team_a"] else 0)
        info.append({
            "year": row["year"],
            "round": row["round"],
            "region": row["region"],
            "team_a": row["team_a"],
            "team_a_seed": row["team_a_seed"],
            "team_b": row["team_b"],
            "team_b_seed": row["team_b_seed"],
            "winner": row["winner"]
        })
    
    return X, y, info