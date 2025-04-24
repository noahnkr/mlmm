import sys
import pandas as pd
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import GridSearchCV, train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
import joblib

from model.utils import load_dataset
from model.eval import (
    evaluate_models, simulate_tournament,
    print_classification_report, print_correct_upsets, 
)
from scraper.utils import YEARS

if "-t" in sys.argv:
    tournament_year = int(sys.argv[2])
    train_years = [y for y in YEARS if y != tournament_year]
    X_train_full, y_train_full, X_test, y_test, info_test = load_dataset(train_years=train_years, test_year=tournament_year)

    # Split off a validation set from the training set
    X_train, X_val, y_train, y_val = train_test_split(X_train_full, y_train_full, test_size=0.2, random_state=42)

    # Define pipeline
    pipeline = Pipeline([
        ('scaler', StandardScaler()),
        ('clf', LogisticRegression(penalty='l1', solver='liblinear', max_iter=1000, class_weight="balanced"))
    ])

    # Hyperparameter tuning
    param_grid = {'clf__C': [0.01, 0.1, 1, 10, 100]}
    grid_search = GridSearchCV(pipeline, param_grid, cv=5, scoring='accuracy')
    grid_search.fit(X_train, y_train)

    best_model = grid_search.best_estimator_
    print("Best parameters:", grid_search.best_params_)

    y_pred = best_model.predict(X_val)
    print("Validation accuracy:", accuracy_score(y_val, y_pred))

    # Save the model
    joblib.dump(best_model, "model/logreg_model.pkl")

    # Simulate tournament with test data
    simulate_tournament(tournament_year, best_model)

elif "-a" in sys.argv:
    total_accuracy = []
    for tournament_year in YEARS:
        train_years = [y for y in YEARS if y != tournament_year]
        X_train, y_train, X_test, y_test, info_test = load_dataset(train_years=train_years, test_year=tournament_year)

        model_acc = evaluate_models(X_train, X_test, y_train, y_test)
        total_accuracy.append(model_acc)

    df = pd.DataFrame(total_accuracy)
