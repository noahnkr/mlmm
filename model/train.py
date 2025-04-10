import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import StandardScaler
from utils import MODELS, load_dataset
from sklearn.metrics import classification_report

X, y = load_dataset()

print(f"Loaded dataset with {len(X)} examples.")

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

print(f"Train size: {len(X_train)}, Test size: {len(X_test)}")

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