import pandas as pd
import numpy as np
from random import shuffle
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score
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

def get_team_vector(year, team, team_stats):
    row = team_stats[(team_stats["year"] == year) & (team_stats["team"] == team)]
    if row.empty:
        return None
    # Remove irrelavent fetures
    return row.drop(columns=["year", "team"]).values.flatten().astype(float)

def load_dataset():
    features, labels = [], []

    matchups = pd.read_csv("data/matchups.csv")
    team_stats = pd.read_csv("data/stats.csv")

    for _, row in matchups.iterrows():
        v_a = get_team_vector(row["year"], row["team_a"], team_stats)
        v_b = get_team_vector(row["year"], row["team_b"], team_stats)

        if v_a is None or v_b is None:
            continue
        
        features.append(v_a - v_b)
        labels.append(row["winner"])
    
    X = np.array(features)
    y = np.array(labels)
    
    return X, y

