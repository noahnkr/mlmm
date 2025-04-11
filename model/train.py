import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from model.utils import TOURNAMENT_YEAR, load_dataset
from model.eval import (
    print_classification_report, print_correct_upsets, simulate_tournament
)
from scraper.utils import YEARS

train_years = [y for y in YEARS if y != TOURNAMENT_YEAR]

X_train, y_train, X_test, y_test, info_test = load_dataset(train_years=train_years, test_year=TOURNAMENT_YEAR)

print(f"Train size: {len(X_train)}, Test size: {len(X_test)}")

model = LogisticRegression(max_iter=1000)
model.fit(X_train, y_train)

preds = model.predict(X_test)

print_classification_report(X_train, X_test, y_train, y_test)
print_correct_upsets(preds, y_test, info_test)
simulate_tournament(TOURNAMENT_YEAR, model)
