import sys
import pandas as pd
from model.utils import load_dataset
from model.eval import (
    evaluate_models, simulate_tournament,
    print_classification_report, print_correct_upsets, 
)
from sklearn.linear_model import LogisticRegression
from scraper.utils import YEARS

if "-t" in sys.argv:
    tournament_year = int(sys.argv[2])
    train_years = [y for y in YEARS if y != tournament_year]
    X_train, y_train, X_test, y_test, info_test = load_dataset(train_years=train_years, test_year=tournament_year)

    model = LogisticRegression(max_iter=1000, class_weight="balanced")
    model.fit(X_train, y_train)

    simulate_tournament(tournament_year, model)
    print_classification_report(X_train, X_test, y_train, y_test)

    preds = model.predict(X_test)
    print_correct_upsets(preds, y_test, info_test)

elif "-a" in sys.argv:

    total_accuracy = []
    for tournament_year in YEARS:
        train_years = [y for y in YEARS if y != tournament_year]
        X_train, y_train, X_test, y_test, info_test = load_dataset(train_years=train_years, test_year=tournament_year)

        model_acc = evaluate_models(X_train, X_test, y_train, y_test)
        total_accuracy.append(model_acc)
    
    df = pd.DataFrame(total_accuracy)
    print("Model Accuracy by Year")
    print(df)
    print("Average Accuracy by Model Across All Years:")
    print(df.mean().round(3))
    

